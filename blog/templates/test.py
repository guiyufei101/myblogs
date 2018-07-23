
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'#默认配置
EMAIL_HOST='smtp.qq.com'
EMAIL_PORT=25
EMAIL_HOST_USER='1963119101@qq.com'
EMAIL_HOST_PASSWORD='gplxsikencuycjcf'#授权码
EMAIL_SUBJECT_PREFIX='[样式博客]'#前缀
EMAIL_USE_TLS = True#与SMTP服务器通信时,是否启动TLS链接（安全链接）

#发送验证码
import string
import random
from django.core.mail import send_mail
code=''.join(random.sample(string.ascii_letters + string.digits,4))
send_mail(
         '绑定邮箱',
         '验证码：%s' % code,
         '1963119101@qq.com',
         '2936739490@qq.com',
         fail_silently=False,
        )
