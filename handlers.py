#coding=utf-8

import json,pdb,datetime,os
from tornado.options import options
from tornado.template import Template
from dxb.handler import TokenAPIHandler,APIHandler,ListCreateAPIHandler,\
    RetrieveUpdateDestroyAPIHandler
import libs.utils as utils
import libs.modellib as model
import models
from mail import send_email

class MailListCreateHandler(ListCreateAPIHandler):
    model = models.MailModel()

class MailRetrieveUpdateDestroyHandler(RetrieveUpdateDestroyAPIHandler):
    model = models.MailModel()

class MailSendHandler(APIHandler):
    models = models.MailModel()

    def post(self):
        result = utils.init_response_data()
        try:
            to_mail_list = json.loads(self.get_argument("to_mail_list","[]"))
            theme = self.get_argument("theme","工作日报")
            template = self.get_argument("template","default")
            template_args = json.loads(self.get_argument("template_args","{}"))
            content = self.generate(template,template_args)
            attachments = []
            request_files = self.request.files
            if request_files.has_key("files"):
                files = request_files["files"]
                for file in files:
                    filename = file.get("filename","")
                    temp_filename_path = os.path.dirname(options.root_path).encode("utf-8") + u"/var/mail/" + filename + u"_" +\
                                         str(datetime.datetime.now()).replace(".","_").replace(":","_").replace(" ","_") + ".xls"
                    temp_mail_file = open(temp_filename_path,"w")
                    temp_mail_file.write(file.get("body",""))
                    attachments.append(dict(
                        filename = u"工作日报.xls",
                        data = temp_filename_path,
                    ))
            print attachments
            send_email('admin@dhui100.com', to_mail_list , theme, '',
                       html=content,
                       attachments=attachments)

        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.write(result)
            self.finish()
            return
        self.finish(result)

    def generate(self,template,template_args):
        content = ""
        return content

handlers = [
    (r"/api/mail/list", MailListCreateHandler),
    (r"/api/mail", MailRetrieveUpdateDestroyHandler),
    (r"/api/mailsend", MailSendHandler),
]