from rest_framework.views import APIView, status
from rest_framework.response import Response
from auth.utils import simpleMessage
from .models import Album, AlbumPhoto, AlbumTag
from datetime import datetime
import json
from django.forms.models import model_to_dict
from bson import ObjectId


class AlbumView(APIView):

    # 抓使用者的所有相簿
    def get(self, request):

        # userId = request.data["userId"]
        userId = request.query_params["userId"]

        albumNameArray = []
        _idArray = []
        coverPhotoIdArray = []

        album = Album.objects(userId=userId).filter()
        print(album.to_json())

        # get albumname
        for a in album:
            if a.isDeleted == False:
                albumNameArray.append(a.albumName)

        # get _id
        for a in album:
            if a.isDeleted == False:
                data = JSONEncoder().encode(a._id)
                data2 = eval(data)
                # print('test:', data2)
                _idArray.append(data2)
        # print(_idArray)

        # get coverPhotoId
        for a in album:
            if a.isDeleted == False:
                # print('test2:', a.coverPhotoId)

                coverPhotoIdArray.append(a.coverPhotoId)

        res = {"albumNameArray": albumNameArray, "_idArray": _idArray,
               "coverPhotoIdArray": coverPhotoIdArray}
        # res = json.dumps(res)
        return Response(res, status=status.HTTP_201_CREATED)

    # CREATE  一鍵建相簿

    def post(self, request):

        album = Album(
            coverPhotoId=request.data['coverPhotoId'],
            albumName=request.data['albumName'],
            userId=request.data['userId'],

        )
        for p in request.data['albumPhoto']:
            album.albumPhoto.append(AlbumPhoto(photoId=p))
        for t in request.data['albumTag']:
            album.albumTag.append(AlbumTag(tag=t))
        album.save()
        return Response(simpleMessage('POST/AlbumView'), status=status.HTTP_201_CREATED)

    # # CREATE 測試建立資料

    # def post(self, request):
    #     """
    #     (測試用)
    #     產生一筆假資料
    #     Args:
    #         None
    #     Returns:
    #         None
    #     """
    #     album = Album(
    #         coverPhotoId='1234579',
    #         albumName='12345',
    #         userId='daioaufio',
    #         albumPhoto=[{'photoId': 'asdfklkajhsl',
    #                      'isDeleted': False},
    #                     {'photoId': 'aagdzzkajhsl',
    #                      'isDeleted': False}],
    #         albumTag=[{'tag': 'album5', 'isDeleted': False}, {
    #             'tag': 'michelle2345', 'isDeleted': False}],
    #         createTime=datetime.utcnow())
    #     album.save()

    #     return Response(simpleMessage('POST/AlbumView'), status=status.HTTP_201_CREATED)

    # 更改相簿名稱

    def put(self, request):

        _id = request.data["_id"]
        albumName = request.data["albumName"]

        try:
            update_rows = Album.objects(_id=_id).update(
                albumName=albumName)
            print(f'Album/View: AlbumView.put, db:{update_rows} rows')
        except Exception as e:
            print(e)
            return Response("AlbumViewError", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(simpleMessage('PUT/AlbumView'), status=status.HTTP_200_OK)

    # 刪除相簿
    def delete(self, request):
        """
        刪除相簿
        把_id的is_delete欄位改成true
        Args:
            request: 裡面需要有_id
        Returns:
            None
        """
        _id = request.data["_id"]

        try:

            update_rows = Album.objects(_id__exact=_id).update(
                isDeleted=True)
            print(f'Album/View: AlbumView.delete, db:{update_rows} rows')

        except Exception as e:
            print(e)
            return Response("AlbumViewError", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(simpleMessage('DELETE/AlbumView'), status=status.HTTP_201_CREATED)


class AlbumTagView(APIView):

    # 取得相簿TAG
    def get(self, request):
        """
        取得相簿的albumTag
        根據_id去更改資料庫的albumTag欄位
        要過濾掉is_delete=true
        Args:
            request: _id
        Returns:
            該album全部的albumTag
        """
        # album_id = request.data["_id"]
        album_id = request.query_params["_id"]

        album_tag_array = []

        try:
            album = Album.objects(_id=album_id).get()

            array_field = album.albumTag

            if len(array_field) == 0:
                print(len(array_field))
                return Response(simpleMessage("zero"), status=status.HTTP_200_OK)

            for single_tag in array_field:
                if single_tag.isDeleted == False:
                    album_tag_array.append(single_tag.tag)
                    print(single_tag.tag)

        except Exception as e:
            print(e)
            return Response(simpleMessage("Get/AlbumTagView: error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print(album_tag_array)
        res = {"result": "Get/AlbumTagView",
               "album_tag": album_tag_array}

        # response_str = json.dumps({"result": "Get/AlbumTagView",
        #                            "album_tag": album_tag_array})

        return Response(res, status=status.HTTP_201_CREATED)

    # 新增相簿TAG
    def post(self, request):
        """
        新增tag時
        根據_id去新增相簿的tag
        會檢查tag是否獨一無二
        Args:
            request: 裡面需要有_id和albumTag
        Returns:
            更改過後的tag
        """
        album_id = request.data["_id"]
        album_tag = request.data["albumTag"]
        print(album_tag)
        tag = {
            'tag': album_tag,
            'isDeleted': False
        }

        try:
            update_rows = Album.objects(_id=album_id).update(
                add_to_set__albumTag=tag)

            print(f'Album/View: TagView.post, db:{update_rows} rows')

        except Exception as e:
            print('error: ', e)
            return Response(simpleMessage("Post/AlbumTagView: error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(simpleMessage('Post/AlbumTagView'), status=status.HTTP_201_CREATED)

    # 刪除相簿TAG
    def delete(self, request):
        """
        刪除tag
        根據_id和albumTag刪掉指定的albumTag
        tag不存在或是成功刪除都會還傳成功
        Args:
            request: 裡面需要有_id和albumTag
        Returns:
            剩下的tag
        """
        album_id = request.data["_id"]
        album_tag = request.data["albumTag"]

        try:

            album = Album.objects(
                _id=album_id, albumTag__match={'tag': album_tag, 'isDeleted': False}).first()
            print(album.to_json())

            for single_tag in album.albumTag:

                if single_tag.tag == album_tag:
                    print('same')
                    single_tag.isDeleted = True
            print(album.to_json())
            album.save()

        except Exception as e:
            print(e)
            return Response(simpleMessage("DELETE/AlbumTagView: error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(simpleMessage('DELETE/AlbumTagView'), status=status.HTTP_201_CREATED)


class AlbumPhotoView(APIView):

    # 抓相簿中的所有照片
    def get(self, request):

        # _id = request.data["_id"]
        _id = request.query_params["_id"]

        album = Album.objects(_id=_id).filter()

        # print(album.to_json())

        # albumNameArray = []
        albumPhotoIdArray = []

        # get albumPhotoId
        for a in album:
            if a.isDeleted == False:
                for z in a.albumPhoto:
                    if z.isDeleted == False:
                    # print(z.photoId)
                        albumPhotoIdArray.append(z.photoId)
        # print(a.albumName)
        print(albumPhotoIdArray)

        # # get albumname
        # for a in album:
        #     if a.isDeleted == False:
        #         albumNameArray.append(a.albumPhoto)
        # # print(a.albumName)
        # print(albumNameArray)


        # # get coverPhotoId
        # for a in album:
        #     if a.isDeleted == False:
        #         print('test2:', a.coverPhotoId)

        #         coverPhotoIdArray.append(a.coverPhotoId)

        res = {"albumPhotoIdArray": albumPhotoIdArray}

        return Response(res, status=status.HTTP_200_OK)

    # 刪除相簿中的相片

    def delete(self, request):
        """
        刪除相簿中的相片
        根據_id和photoId刪掉指定的相片
        photo不存在或是成功刪除都會還傳成功
        Args:
            request: 裡面需要有_id和photoId
        Returns:
            相簿剩下的photo
        """

        album_id = request.data["_id"]
        album_photo = request.data["albumPhoto"]

        try:

            album = Album.objects(
                _id=album_id, albumPhoto__match={'photoId': album_photo, 'isDeleted': False}).first()
            print(album.to_json())

            for single_photo in album.albumPhoto:

                if single_photo.photoId == album_photo:
                    print('same')
                    single_photo.isDeleted = True
            print(album.to_json())
            album.save()

        except Exception as e:
            print(e)
            return Response(simpleMessage("DELETE/AlbumPhotoView: error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(simpleMessage('DELETE/AlbumPhotoView'), status=status.HTTP_201_CREATED)

    # 新增相片到相簿中(現在先不用這個，只有一鍵建相簿)
    def post(self, request):
        """
        新增photo時
        根據_id去新增相簿的photo
        會檢查photo是否獨一無二
        Args:
            request: 裡面需要有_id和photoId
        Returns:
            更改過後的photo
        """
        album_id = request.data["_id"]
        album_photo = request.data["albumPhoto"]
        photoId = {
            'photoId': album_photo,
            'isDeleted': False
        }

        try:
            update_rows = Album.objects(_id=album_id).update(
                add_to_set__albumPhoto=photoId)

            print(f'Album/View: AlbumPhotoView.post, db:{update_rows} rows')

        except Exception as e:
            print('error: ', e)
            return Response(simpleMessage("Post/AlbumPhotoView: error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(simpleMessage('Post/AlbumPhotoView'), status=status.HTTP_201_CREATED)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
