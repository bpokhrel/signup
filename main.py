#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE=re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE=re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>SignUp</h1>
    """

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # a form for labeling
        add_form = """
        <form action="/signup" method="post">
            <label>
                Username
                <input type="text" name="username" value="" required=""/>
            </label>
            <br><br>
        <label>
            Password
            <input type="password" name="password" value="" required=""/>
        </label>
        <br><br>
        <label>
            Verify Password
            <input type="password" name="verify" value="" required=""/>
        </label>
        <br><br>
        <label>
            Email(Optional)
            <input type="text" name="email" value=""/>
        </label>
        <br><br>
            <input type="submit" value="Submit Query"/>
        </form>
        """
        error = self.request.get("error")
        error_element = "<p class='error'>"+ error + "</p>" if error else ""

        content=page_header+add_form+error_element+page_footer
        self.response.write(content)

welcome_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome Page</title>
</head>
<body>
   <h1></h1>
    """

class SignUp(webapp2.RequestHandler):

    def post(self):
        username=self.request.get("username")
        password=self.request.get("password")
        verify=self.request.get("verify")
        email=self.request.get("email")

        if not valid_username(username):
            error = "That's not a valid username."
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        elif not valid_password(password):
            error="That's not a valid password."
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        elif password!=verify:
            error="Your passwords didn't match"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        elif not valid_email(email):
            error="That's not a valid email."
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        else:
            self.redirect("/welcome?username= "+username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        self.response.write(welcome_header+"""<h1>"""+"""Welcome, """+username+"""</h1>"""+page_footer)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup',SignUp),
    ('/welcome',Welcome)
], debug=True)
