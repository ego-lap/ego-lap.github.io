#!/usr/bin/env python3
"""Regenerate the two vector summary plots from verified reported results.

Requires matplotlib. No uncertainty estimates are added. The GRPO values
are relative improvements, as labeled in the original source figure.
"""
from pathlib import Path
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
plt.rcParams.update({'svg.fonttype':'none','font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.labelcolor':'#637067','xtick.color':'#798279','ytick.color':'#34473d'})
def chart(name,labels,values,title,xlabel):
 fig,ax=plt.subplots(figsize=(6,3.6));fig.patch.set_facecolor('white');ax.set_facecolor('white')
 bars=ax.barh(range(len(labels)),values,color=['#28624d']+['#a8beae']*(len(values)-1),height=.46)
 ax.set_yticks(range(len(labels)),labels);ax.invert_yaxis();ax.set_xlim(0,23);ax.set_xticks([0,5,10,15,20],[str(v)+'%' for v in [0,5,10,15,20]])
 ax.tick_params(axis='both',length=0,pad=12);ax.set_axisbelow(True);ax.grid(axis='x',color='#e4eae3',linewidth=.8)
 for b,v in zip(bars,values):ax.text(v+.5,b.get_y()+b.get_height()/2,f'{v:.1f}%',va='center',color='#28624d',weight='bold',fontsize=12)
 ax.set_xlabel(xlabel,labelpad=15,fontsize=10);fig.tight_layout(pad=1.7)
 fig.savefig(root/'assets/images'/name,format='svg',metadata={'Title':title,'Description':'Values from the current EgoLAP paper; reproduced as vectors without added error bars.'});plt.close(fig)
chart('human-data-transfer.svg',['Human + robot data','Robot data only'],[16.4,7.2],'Human data improves zero-shot simulation transfer','Zero-shot simulation success rate')
chart('grpo-improvement.svg',['Reasoning pre-training\nLanguage actions only','Reasoning pre-training\nReasoning + actions','No reasoning\npre-training'],[19.4,12.7,14.2],'GRPO post-training improves simulation performance','Relative improvement after GRPO')
