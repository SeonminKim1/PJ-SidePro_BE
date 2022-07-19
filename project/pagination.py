# article/pagination.py
from rest_framework.pagination import PageNumberPagination

class BasePagination(PageNumberPagination):
    # 페이지 사이즈를 지정할 query_param 문자열 지정 ex) /?page_size=5
    page_size_query_param = 'page_size'

class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        # 페이지네이터와 연결된 뷰 확인 hasattr(속성 포함 여부 확인)
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    
    def paginate_queryset(self, queryset):
        # 결과 한 페이지를 반환하거나, 페이지 분할을 사용하지 않을 경우 '없음'을 반환합니다.
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        # 지정된 출력 데이터에 대해 페이지 유형 'Response' 개체를 반환합니다.
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)