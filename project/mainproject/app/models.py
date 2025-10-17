from django.db import models
from django.conf import settings


class Class_cancellation(models.Model):
    date = models.DateTimeField("休講情報")
    
class Homework(models.Model):
    deadline = models.DateTimeField("締め切り")
    content = models.TextField("内容", blank=True)
    
class Memo(models.Model):
    content = models.TextField("内容", blank=True)
    # image = models.ImageField("画像", upload_to='memo_images/', blank=True, null=True)
    
class Class(models.Model):
    class_name = models.CharField("授業名", max_length=100)
    professor_name = models.CharField("教授名", max_length=100)
    classroom_name = models.CharField("教室名", max_length=100)
    
    day_of_the_week = models.IntegerField("曜日", choices=[
        (0, '日曜日'),
        (1, '月曜日'),
        (2, '火曜日'),
        (3, '水曜日'),
        (4, '木曜日'),
        (5, '金曜日'),
        (6, '土曜日'),
    ])
    period = models.IntegerField("時限", choices=[
        (1, "1限目"),
        (2, "2限目"),
        (3, "3限目"),
        (4, "4限目"),
        (5, "5限目"),
        (6, "6限目"),
        (7, "7限目"),
        (8, "8限目"),
    ])
    
    attendance_count = models.IntegerField("出席回数", default=0)
    absence_count = models.IntegerField("欠席回数", default=0)
    total_late_and_early_leave_count = models.IntegerField("遅刻・早退回数", default=0)
    belongings = models.TextField("持ち物", blank=True)
    class_cancellations = models.ForeignKey(Class_cancellation, on_delete=models.CASCADE, verbose_name="休講情報", blank=True, null=True)
    homeworks = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name="宿題", blank=True, null=True)
    examination = models.TextField("試験日程", blank=True)
    memos = models.ForeignKey(Memo, on_delete=models.CASCADE, verbose_name="メモ", blank=True, null=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="作成者",
    )
    
    # 管理画面に授業名を表示
    def __str__(self):
        return self.class_name
    

