#!/usr/bin/python3
import turtle, time

N = 300
CLOCK_BORDER_WIDTH = N/10
HOUR_HAND_LEN = N/2
HOUR_HAND_WIDTH = N/12
MIN_HAND_LEN = N/1.4
MIN_HAND_WIDTH = N/18
SEC_HAND_LEN = N/1.1
SEC_HAND_WIDTH = N/30
MIN_INDICATORS_LEN = N/7
SEC_INDICATORS_LEN = N/10

clock = turtle.Turtle(); clock.speed(0); clock.width(CLOCK_BORDER_WIDTH); clock.color('blue')
clock.lt(90); clock.up(); clock.fd(N); clock.rt(90); clock.down(); clock.circle(-N)

clock.width(N/20)
for i in range(12):
	clock.circle(-N, 30); clock.rt(90); clock.fd(MIN_INDICATORS_LEN); clock.bk(MIN_INDICATORS_LEN); clock.lt(90)
clock.width(N/40)
for i in range(1, 61):
	clock.circle(-N, 6); clock.rt(90)
	if i % 5 != 0:
		clock.fd(SEC_INDICATORS_LEN); clock.bk(SEC_INDICATORS_LEN)
	clock.lt(90)

HT = turtle.Turtle(); HT.width(HOUR_HAND_WIDTH); HT.speed(0)
MT = turtle.Turtle(); MT.width(MIN_HAND_WIDTH); MT.speed(0)
ST = turtle.Turtle(); ST.width(SEC_HAND_WIDTH); ST.speed(0)

def H(): return int(time.strftime('%H'))
def M(): return int(time.strftime('%M'))
def S(): return int(time.strftime('%S'))
def DegToDir(deg): return 90-deg

def drawH(h, m): HT.seth(DegToDir((h*30)+(m/2))); HT.fd(HOUR_HAND_LEN)
def drawM(m): MT.seth(DegToDir(m*6)); MT.fd(MIN_HAND_LEN)
def drawS(s): ST.seth(DegToDir(s*6)); ST.fd(SEC_HAND_LEN)

h = H(); m = M(); s = S()
drawH(h,m); drawM(m); drawS(s)

while 1:
	tmph = H(); tmpm = M(); tmps = S()
	if tmps != s:
		ST.undo(); ST.undo(); drawS(tmps)
		if tmpm != m:
			MT.undo(); MT.undo(); drawM(tmpm)
			HT.undo(); HT.undo(); drawH(tmph, tmpm)
			m = tmpm
		s = tmps
