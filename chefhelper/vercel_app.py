#!/usr/bin/env python3
import os
import sys

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')

import streamlit as st
import openai
import pandas as pd
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

# ... rest of the app code is in app.py
