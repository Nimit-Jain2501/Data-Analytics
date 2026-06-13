"""
NayePankh Foundation – Data Analytics Project
================================================
Sections:
  1. Load & Clean Data
  2. Beneficiary Analysis
  3. Donation Trends
  4. Volunteer Insights
  5. Program Performance
  6. Combined Dashboard (saved as PNG)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Style ────────────────────────────────────────────────────
ORANGE  = '#FF6B35'
BLUE    = '#1D3557'
GREEN   = '#2DC653'
YELLOW  = '#FFC300'
LIGHT   = '#F0F4F8'
GRAY    = '#6C757D'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   LIGHT,
    'axes.grid':        True,
    'grid.color':       'white',
    'grid.linewidth':   1.2,
    'font.family':      'DejaVu Sans',
    'axes.spines.top':  False,
    'axes.spines.right':False,
})

DATA = '/home/claude/nayepankh_analytics/data'
OUT  = '/home/claude/nayepankh_analytics/outputs'

# ─────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────
ben  = pd.read_csv(f'{DATA}/beneficiaries.csv', parse_dates=['enrollment_date'])
don  = pd.read_csv(f'{DATA}/donations.csv',     parse_dates=['donation_date'])
vol  = pd.read_csv(f'{DATA}/volunteers.csv',    parse_dates=['join_date'])
prog = pd.read_csv(f'{DATA}/programs.csv')

don['year']    = don['donation_date'].dt.year
don['month']   = don['donation_date'].dt.month
don['quarter'] = don['donation_date'].dt.to_period('Q').astype(str)
ben['year']    = ben['enrollment_date'].dt.year

print("Data loaded ✅")
print(f"  Beneficiaries: {len(ben)} | Donations: {len(don)} | Volunteers: {len(vol)} | Programs: {len(prog)}")

# ─────────────────────────────────────────────────────────────
# 2. KPI SUMMARY
# ─────────────────────────────────────────────────────────────
total_donations    = don['amount'].sum()
total_beneficiaries = len(ben)
active_volunteers  = vol[vol['status'] == 'Active'].shape[0]
programs_run       = prog['program_name'].nunique()
avg_success        = prog['success_rate'].mean() * 100
total_scholarship  = ben['scholarship_amount'].sum()

print("\n📊 KEY PERFORMANCE INDICATORS")
print(f"  Total Donations      : ₹{total_donations:,.0f}")
print(f"  Total Beneficiaries  : {total_beneficiaries}")
print(f"  Active Volunteers    : {active_volunteers}")
print(f"  Programs Running     : {programs_run}")
print(f"  Avg Success Rate     : {avg_success:.1f}%")
print(f"  Total Scholarships   : ₹{total_scholarship:,.0f}")

# ─────────────────────────────────────────────────────────────
# 3. VISUALIZATIONS – MAIN DASHBOARD
# ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 24))
fig.patch.set_facecolor('white')

# Title banner
fig.text(0.5, 0.98, 'NayePankh Foundation', ha='center', va='top',
         fontsize=28, fontweight='bold', color=BLUE)
fig.text(0.5, 0.965, 'Data Analytics Dashboard  |  2021 – 2023',
         ha='center', va='top', fontsize=14, color=GRAY)

gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35,
                       top=0.95, bottom=0.04, left=0.06, right=0.97)

# ── KPI Cards (Row 0) ────────────────────────────────────────
kpis = [
    (f"₹{total_donations/1e5:.1f}L",  "Total Donations",     ORANGE),
    (f"{total_beneficiaries}",         "Beneficiaries Served", BLUE),
    (f"{active_volunteers}",           "Active Volunteers",    GREEN),
    (f"₹{total_scholarship/1e5:.1f}L", "Scholarships Awarded", YELLOW),
    (f"{avg_success:.1f}%",            "Avg Program Success",  '#9B59B6'),
    (f"{programs_run}",                "Programs Running",     '#E74C3C'),
]
for col, (val, label, color) in enumerate(kpis[:3]):
    ax = fig.add_subplot(gs[0, col])
    ax.set_facecolor(color)
    ax.text(0.5, 0.6, val,   ha='center', va='center', transform=ax.transAxes,
            fontsize=26, fontweight='bold', color='white')
    ax.text(0.5, 0.2, label, ha='center', va='center', transform=ax.transAxes,
            fontsize=11, color='white', alpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)

# ── Donation Trend by Quarter (Row 1, span 2 cols) ───────────
ax1 = fig.add_subplot(gs[1, :2])
q_don = don.groupby('quarter')['amount'].sum().reset_index()
q_don = q_don.sort_values('quarter')
bars = ax1.bar(q_don['quarter'], q_don['amount']/1000, color=ORANGE, edgecolor='white', width=0.6)
ax1.set_title('Quarterly Donation Trend', fontsize=13, fontweight='bold', color=BLUE, pad=10)
ax1.set_xlabel('Quarter', color=GRAY); ax1.set_ylabel('Amount (₹ Thousands)', color=GRAY)
ax1.tick_params(axis='x', rotation=45, labelsize=8)
for bar in bars:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'₹{bar.get_height():.0f}K', ha='center', va='bottom', fontsize=7, color=BLUE)

# ── Donor Type Breakdown (Row 1, col 2) ──────────────────────
ax2 = fig.add_subplot(gs[1, 2])
dtype = don.groupby('donor_type')['amount'].sum()
colors_pie = [ORANGE, BLUE, GREEN, YELLOW, '#9B59B6']
wedges, texts, autotexts = ax2.pie(dtype.values, labels=dtype.index, autopct='%1.1f%%',
                                    colors=colors_pie, startangle=140,
                                    textprops={'fontsize': 8})
for at in autotexts: at.set_color('white'); at.set_fontweight('bold')
ax2.set_title('Donations by Donor Type', fontsize=13, fontweight='bold', color=BLUE)

# ── Beneficiaries by Program (Row 2, col 0) ──────────────────
ax3 = fig.add_subplot(gs[2, 0])
prog_count = ben.groupby('program').size().sort_values()
ax3.barh(prog_count.index, prog_count.values, color=BLUE, edgecolor='white')
ax3.set_title('Beneficiaries by Program', fontsize=12, fontweight='bold', color=BLUE)
ax3.set_xlabel('Count', color=GRAY)
for i, v in enumerate(prog_count.values):
    ax3.text(v+1, i, str(v), va='center', fontsize=8, color=BLUE)

# ── Gender Distribution (Row 2, col 1) ───────────────────────
ax4 = fig.add_subplot(gs[2, 1])
gender = ben['gender'].value_counts()
ax4.bar(gender.index, gender.values, color=[GREEN, ORANGE, YELLOW], edgecolor='white', width=0.5)
ax4.set_title('Beneficiary Gender Split', fontsize=12, fontweight='bold', color=BLUE)
ax4.set_ylabel('Count', color=GRAY)
for i, v in enumerate(gender.values):
    ax4.text(i, v+2, str(v), ha='center', fontsize=9, color=BLUE, fontweight='bold')

# ── State-wise Beneficiaries (Row 2, col 2) ──────────────────
ax5 = fig.add_subplot(gs[2, 2])
state_count = ben['state'].value_counts().head(7)
ax5.bar(state_count.index, state_count.values, color=ORANGE, edgecolor='white')
ax5.set_title('Top States – Beneficiaries', fontsize=12, fontweight='bold', color=BLUE)
ax5.set_ylabel('Count', color=GRAY)
ax5.tick_params(axis='x', rotation=30, labelsize=8)

# ── Program Success Rate (Row 3, col 0:2) ────────────────────
ax6 = fig.add_subplot(gs[3, :2])
prog_success = prog.groupby('program_name')['success_rate'].mean().sort_values() * 100
colors_bar = [GREEN if v >= 80 else YELLOW if v >= 70 else ORANGE for v in prog_success.values]
bars6 = ax6.barh(prog_success.index, prog_success.values, color=colors_bar, edgecolor='white')
ax6.axvline(80, color='red', linestyle='--', linewidth=1.5, label='80% Target')
ax6.set_title('Average Program Success Rate (%)', fontsize=12, fontweight='bold', color=BLUE)
ax6.set_xlabel('Success Rate (%)', color=GRAY)
ax6.legend(fontsize=9)
for bar in bars6:
    ax6.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
             f'{bar.get_width():.1f}%', va='center', fontsize=9, color=BLUE)

# ── Volunteer Hours by Role (Row 3, col 2) ───────────────────
ax7 = fig.add_subplot(gs[3, 2])
vol_hours = vol.groupby('role')['hours_contributed'].sum().sort_values()
ax7.barh(vol_hours.index, vol_hours.values, color='#9B59B6', edgecolor='white')
ax7.set_title('Volunteer Hours by Role', fontsize=12, fontweight='bold', color=BLUE)
ax7.set_xlabel('Total Hours', color=GRAY)
ax7.tick_params(axis='y', labelsize=8)

plt.savefig(f'{OUT}/nayepankh_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("\n✅ Dashboard saved: outputs/nayepankh_dashboard.png")

# ─────────────────────────────────────────────────────────────
# 4. TREND ANALYSIS CHART
# ─────────────────────────────────────────────────────────────
fig2, axes = plt.subplots(1, 2, figsize=(16, 5))
fig2.suptitle('NayePankh Foundation – Trend Analysis', fontsize=16, fontweight='bold', color=BLUE)

# Monthly donation trend
monthly = don.groupby(['year','month'])['amount'].sum().reset_index()
monthly['period'] = pd.to_datetime(monthly[['year','month']].assign(day=1))
axes[0].plot(monthly['period'], monthly['amount']/1000, color=ORANGE, linewidth=2.5, marker='o', markersize=4)
axes[0].fill_between(monthly['period'], monthly['amount']/1000, alpha=0.15, color=ORANGE)
axes[0].set_title('Monthly Donation Trend', fontsize=13, fontweight='bold', color=BLUE)
axes[0].set_xlabel('Month'); axes[0].set_ylabel('Amount (₹ Thousands)')
axes[0].tick_params(axis='x', rotation=30)

# Enrollment trend
enroll = ben.groupby(['year', ben['enrollment_date'].dt.month])['beneficiary_id'].count().reset_index()
enroll.columns = ['year','month','count']
enroll['period'] = pd.to_datetime(enroll[['year','month']].assign(day=1))
for yr, grp in enroll.groupby('year'):
    axes[1].plot(grp['month'], grp['count'], label=str(yr), linewidth=2, marker='s', markersize=5)
axes[1].set_title('Monthly Beneficiary Enrollments by Year', fontsize=13, fontweight='bold', color=BLUE)
axes[1].set_xlabel('Month'); axes[1].set_ylabel('New Enrollments')
axes[1].legend(title='Year'); axes[1].set_xticks(range(1,13))
axes[1].set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=30)

plt.tight_layout()
plt.savefig(f'{OUT}/trend_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Trend chart saved: outputs/trend_analysis.png")

# ─────────────────────────────────────────────────────────────
# 5. PRINT SUMMARY REPORT
# ─────────────────────────────────────────────────────────────
report = f"""
╔══════════════════════════════════════════════════════╗
║       NAYEPANKH FOUNDATION – ANALYTICS REPORT       ║
║               Period: 2021 – 2023                   ║
╠══════════════════════════════════════════════════════╣
║  IMPACT METRICS                                     ║
║  ▸ Beneficiaries Served   : {total_beneficiaries:<6}                 ║
║  ▸ Active Volunteers      : {active_volunteers:<6}                 ║
║  ▸ Programs Operational   : {programs_run:<6}                 ║
║                                                     ║
║  FINANCIAL HIGHLIGHTS                               ║
║  ▸ Total Donations Raised : ₹{total_donations:>10,.0f}           ║
║  ▸ Total Scholarships     : ₹{total_scholarship:>10,.0f}           ║
║  ▸ Avg Donation (Monthly) : ₹{don.groupby(don['donation_date'].dt.to_period('M'))['amount'].sum().mean():>10,.0f}           ║
║                                                     ║
║  PROGRAM EFFECTIVENESS                              ║
║  ▸ Average Success Rate   : {avg_success:>6.1f}%               ║
║  ▸ Top Program            : {prog.groupby('program_name')['success_rate'].mean().idxmax():<21}║
║  ▸ Highest Enrolled State : {ben['state'].value_counts().idxmax():<21}║
╚══════════════════════════════════════════════════════╝
"""
print(report)
with open(f'{OUT}/summary_report.txt', 'w') as f:
    f.write(report)
print("✅ Text report saved: outputs/summary_report.txt")
print("\n🎉 All analysis complete! Check the outputs/ folder.")
