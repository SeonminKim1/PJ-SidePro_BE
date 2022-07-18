# project(app)/models.py
from datetime import timedelta
from datetime import datetime
from django.db import models
from user.models import User, Skills


# 프로젝트(게시글)
class Project(models.Model):
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    skills = models.ManyToManyField(Skills, verbose_name="카테고리")
    thumnail_img_path = models.FileField(upload_to="", verbose_name="썸네일")
    content = models.TextField("글내용")
    count = models.PositiveIntegerField("조회수")
    github_url = models.URLField("레포지토리주소")
    created_date = models.DateTimeField("생성날짜", auto_now_add=True)
    updated_date = models.DateTimeField("수정날짜", auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "PROJECT"

# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name="게시글", on_delete=models.CASCADE)
    comment = models.TextField("댓글내용")
    created_date = models.DateTimeField("작성날짜", auto_now_add=True)
    updated_date = models.DateTimeField("수정날짜", auto_now=True)
    
    def __str__(self):
        return (f"{self.user} / {self.project} / {self.comment}")
    
    class Meta:
        db_table = "COMMENT"