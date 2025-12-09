from django.db import models
from django.conf import settings

class Class(models.Model):
    class_name = models.CharField("授業名", max_length=100)
    professor_name = models.CharField("教授名", max_length=100, blank=True, null=True)
    classroom_name = models.CharField("教室名", max_length=100, blank=True, null=True)
    
    attendance_count = models.IntegerField("出席回数", default=0)
    absence_count = models.IntegerField("欠席回数", default=0)
    total_late_and_early_leave_count = models.IntegerField("遅刻・早退回数", default=0)
    belongings = models.TextField("持ち物", blank=True, null=True)
    examination = models.DateField("試験日程", blank=True, null=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="作成者",
    )
    
    # 管理画面に授業名を表示
    def __str__(self):
        return self.class_name
    

class Class_schedule(models.Model):
    
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, blank=False, null=False)

    day_of_the_week = models.IntegerField("曜日", choices=[
        (0, '月曜日'),
        (1, '火曜日'),
        (2, '水曜日'),
        (3, '木曜日'),
        (4, '金曜日'),
        (5, '土曜日')
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
    def __str__(self):
        return f"スケジュール: {self.day_of_the_week}曜日 {self.period}限目"

class Class_cancellation(models.Model):
    date = models.DateField("休講情報")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"休講日: {self.date.strftime('%Y-%m-%d')}"

    
class Homework(models.Model):
    deadline = models.DateField("締め切り")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    content = models.TextField("内容", blank=True)
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.content[:20]  # 先頭の20文字を表示

    
class Memo(models.Model):
    content = models.TextField("内容", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE,  blank=True, null=True)
    
    def __str__(self):
        return self.content[:20]  # 先頭の20文字を表示

    
