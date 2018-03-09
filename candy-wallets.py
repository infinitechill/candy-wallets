#!/usr/local/bin/python3

# pip install ecdsa
# pip install pysha3
# pip install pyqrcode
# pip install pypng
# pip install reportlab
# pip install pillow


"""
Neon Purple Color Palette
#000000	(0,0,0)
#7d12ff	(125,18,255)
#ab20fd	(171,32,253)
#200589	(32,5,137)
"""

from ecdsa import SigningKey, SECP256k1
import sha3
import pyqrcode
import png
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

keccak = sha3.keccak_256()

priv = SigningKey.generate(curve=SECP256k1)
pub = priv.get_verifying_key().to_string()

keccak.update(pub)
address = keccak.hexdigest()[24:]

private_key=priv.to_string().hex()
public_key=pub.hex()

address_code = pyqrcode.create("0x"+address, error='L', version=27, mode='binary')
address_code.png('code.png', scale=2, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
#address_code.show()

qr_code_file='code.png'

qr_path = os.path.expanduser(qr_code_file)
logo_path = os.path.expanduser('logo.png')

im = Image.open(qr_code_file)
qr_width, qr_height = im.size

canvas = canvas.Canvas("form.pdf", pagesize=landscape(letter))

canvas.setFillColor((HexColor("#ab20fd")))

path = canvas.beginPath()
path.moveTo(-5*cm,-5*cm)
path.lineTo(-5*cm,35*cm)
path.lineTo(35*cm,35*cm)
path.lineTo(35*cm,-5*cm)
canvas.drawPath(path,True,True)

canvas.setLineWidth(.9)
canvas.setFont('Helvetica', 10)
canvas.setFillColorRGB(32,5,137)

#canvas.drawInlineImage('image.png', 0,0, width=500,height=200) 

canvas.drawString(35,550,'Address:')
canvas.drawString(35,540,address)

canvas.drawString(35,530,'Private Key:')
canvas.drawString(35,520,private_key)

canvas.drawString(35,510,'Public Key:')
canvas.drawString(35,500,public_key)

scaler=.75
canvas.drawInlineImage('code.png', 25,250, width=qr_width*scaler,height=qr_height*scaler) 
canvas.drawInlineImage('logo.png', qr_width*scaler+25,250, width=qr_width*scaler,height=qr_height*scaler) 
canvas.drawInlineImage('code.png', qr_width*scaler+qr_width*scaler+25,250, width=qr_width*scaler,height=qr_height*scaler) 

canvas.save()

pdf = "form.pdf"
previewPath = r'/Applications/Preview.app'
subprocess.Popen([previewPath, pdf])
