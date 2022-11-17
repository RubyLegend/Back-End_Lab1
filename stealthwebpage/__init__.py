from flask import Flask
app = Flask(__name__)

import stealthwebpage.views
import stealthwebpage.db