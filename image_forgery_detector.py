import streamlit as st
from transformers import pipeline
import wikipedia
from PIL import Image
import urllib.parse  

# إعداد ويكيبيديا للعربية
wikipedia.set_lang("ar")

@st.cache_resource
def load_vision_model():
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

captioner = load_vision_model()

st.title("🏛️ المرشد السياحي البصري الذكي")
st.write("ارفع صورة المكان، وسأتعرف عليه وأعطيك تقريراً ورابط فيديو لشرحه.")

file = st.file_uploader("اختر صورة المعلم السياحي:", type=['jpg', 'png', 'jpeg'])

if file:
    img = Image.open(file).convert('RGB')
    st.image(img, use_container_width=True)
    
    with st.spinner(" جاري التعرف على الصورة وتوليد المعلومات..."):
        try:
            # أ- التعرف على ما في الصورة
            result = captioner(img)
            name_en = result[0]['generated_text']
            
            # ب- البحث عن المعلومات في ويكيبيديا
            search_results = wikipedia.search(name_en)
            if search_results:
                page = wikipedia.page(search_results[0])
                report = wikipedia.summary(search_results[0], sentences=4)
                
                st.subheader(f"📍 المعلم المكتشف: {page.title}")
                st.success(report)
                
                # --- : إضافة رابط فيديو ---
                st.divider() # خط فاصل للتنظيم
                st.markdown("  شاهد فيديو عن هذا المكان")
                
                # إنشاء رابط بحث في يوتيوب باستخدام اسم المعلم المكتشف
                search_query = urllib.parse.quote(page.title)
                youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
                
                # عرض الرابط كـ زر جذاب
                st.video_link = f"اضغط هنا لمشاهدة فيديوهات عن {page.title} على يوتيوب"
                st.link_button(f" مشاهدة شروحات فيديو عن {page.title}", youtube_url)
                
            else:
                st.warning("تعرفت على الصورة ولكن لم أجد معلومات تفصيلية عنها.")
                
        except Exception as e:
            st.error("حدث خطأ في معالجة المعلومات.")

st.sidebar.info("هذا النظام يجمع بين الرؤية الحاسوبية وقاعدة بيانات المعلومات العالمية.")