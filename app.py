import streamlit as st
import time
import pandas as pd
import numpy as np
from tools import reduce_motor_speed_api, create_work_order_api

# إعدادات الصفحة
st.set_page_config(
    page_title="رَصِين | Raseen AI Agent",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيقات الواجهة (CSS)
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E88E5; text-align: right; }
    .sub-title { font-size: 1rem; color: #555555; text-align: right; margin-bottom: 25px; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-title">⚙️ منصة رَصِين | Autonomous Predictive Maintenance Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نظام الوكيل الذكي للتحليل الاستباقي واتخاذ القرارات الآلية للمعدات الصناعية</div>', unsafe_allow_html=True)

# القائمة الجانبية لحساسات IoT
st.sidebar.header("🎛️ محاكاة الحساسات (IoT Telemetry)")
temp = st.sidebar.slider("🌡️ درجة الحرارة (°C)", 40, 130, 85)
vib = st.sidebar.slider("📳 مستوى الاهتزاز (mm/s)", 0.5, 10.0, 3.5)
rpm = st.sidebar.slider("🔄 سرعة الدوران (RPM)", 500, 3000, 1800)

# حساب المؤشرات التشغيلية
rul = max(0, int(120 - (temp * 0.7 + vib * 5.5)))
csi = min(100, int((temp / 130) * 55 + (vib / 10.0) * 45))

# عرض المؤشرات
col1, col2, col3 = st.columns(3)
col1.metric("العمر المتبقي (RUL)", f"{rul} ساعة", delta="- حرج" if rul < 25 else "طبيعي", delta_color="inverse")
col2.metric("مؤشر الإجهاد (CSI)", f"{csi}%", delta="+ مرتفع" if csi > 65 else "آمن", delta_color="inverse")
col3.metric("حالة التشغيل", "🚨 خطر" if csi > 65 else "🟢 مستقر")

st.divider()

left_col, right_col = st.columns([1, 1])

# رسم البياني
with left_col:
    st.subheader("📊 قراءات الحساسات اللحظية")
    chart_data = pd.DataFrame(
        np.random.randn(25, 2) / [12, 2.5] + [temp, vib],
        columns=['درجة الحرارة °C', 'الاهتزاز mm/s']
    )
    st.line_chart(chart_data)

# منطق الـ AI Agent
with right_col:
    st.subheader("🤖 سجل تفكير واتخاذ القرار (AI Reasoning)")
    if st.button("🚀 تشغيل الـ AI Agent للتحليل والتنفيذ", type="primary", use_container_width=True):
        with st.status("🧠 [Reasoning Loop] جاري تقييم المخاطر واستدعاء الأدوات...", expanded=True) as status:
            st.write(f"🔍 **1. Sensing:** قراءة الحساسات الحالية: الحرارة = {temp}°C، الاهتزاز = {vib} mm/s.")
            time.sleep(1)
            st.write(f"📐 **2. ML Evaluation:** حساب مؤشر الإجهاد CSI = **{csi}%** والعمر المتبقي RUL = **{rul} ساعة**.")
            time.sleep(1)
            
            if csi > 65:
                st.write("⚠️ **3. Anomaly Detected:** القراءات تجاوزت حدود الأمان المسموح بها!")
                time.sleep(1)

                st.write("🧠 **4. Agent Decision:** تم اتخاذ قرار بتخفيف حمل المحرك وإنشاء امر صيانة.")
                time.sleep(1)

                # ============================
                # TOOL 1: Reduce Motor Speed
                # ============================
                st.write("⚙️ **Autonomous Tool Call:** تشغيل أداة خفض سرعة المحرك...")
                motor_result = reduce_motor_speed_api(current_rpm=rpm, reduction_percent=30)

                if motor_result["success"]:
                    st.success(f"✅ {motor_result['message']}")
                    st.write(f"📊 السرعة السابقة: **{motor_result['old_rpm']} RPM** | السرعة الجديدة: **{motor_result['new_rpm']} RPM**")

                time.sleep(1)

                # ============================
                # TOOL 2: Create Work Order
                # ============================
                st.write("✉️ **Autonomous Tool Call:** إنشاء أمر صيانة تلقائي...")
                work_order_result = create_work_order_api(priority="HIGH", equipment="Motor-01")

                if work_order_result["success"]:
                    st.success(f"🔧 {work_order_result['message']}")
                    st.write(f"الأولوية: **{work_order_result['priority']}** | الحالة: **{work_order_result['status']}**")

                time.sleep(1)

                status.update(label="🚨 تم التدخل الآلي بنجاح!", state="error")
                st.error("🤖 تم اكتشاف الخطر، وتخفيف سرعة المحرك، وإنشاء أمر صيانة تلقائيًا.")
            else:
                st.write("🟢 **3. Status Normal:** جميع المؤشرات ضمن النطاق الآمن.")
                time.sleep(1)
                status.update(label="✅ المحرك يعمل بكفاءة واستقرار تام", state="complete")
                st.success("✨ لا تتطلب المعدة أي تدخل حاليًا.")
