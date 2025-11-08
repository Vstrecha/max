<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Row } from 'vant'
import AvatarImage from '@/components/utility/AvatarImage.vue'
import QRCodeVue from 'qrcode.vue'
import { getLandingPreview } from '@/controllers/max'

const props = defineProps<{
  text?: string
  description?: string
}>()

const route = useRoute()
const router = useRouter()

const qrText = computed(() => props.text ?? (route.query.text as string | undefined) ?? '')
const qrDescription = computed(
  () => props.description ?? (route.query.description as string | undefined) ?? '',
)

const preview = getLandingPreview()

const goBack = () => {
  router.back()
}
</script>

<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <img class="background-effect-1" src="@/assets/icons/background-effect-hills.svg" />
      <img class="background-effect-2" src="@/assets/icons/background-effect-polylines.svg" />
      <div class="content">
        <Row justify="center">
          <div class="logo_wrap">
            <img class="logo_icon" src="@/assets/icons/vstrecha-icon.svg" alt="Встреча!" />
            <span class="logo_header">Встреча!</span>
          </div>
        </Row>

        <div class="qr_wrap">
          <QRCodeVue v-if="qrText" :value="qrText" :size="220" :level="'M'" class="qr_code" />
          <div v-else class="qr_placeholder">
            <AvatarImage
              width="140px"
              height="140px"
              border-weight="3"
              :avatar_url="preview.avatar_url"
              :signature="preview.name"
            />
            <span class="qr_placeholder_text">Нет данных для QR-кода</span>
          </div>
        </div>

        <p v-if="qrDescription" class="description">{{ qrDescription }}</p>

        <div class="button_wrap">
          <Button type="primary" size="large" @click="goBack">Назад</Button>
        </div>
      </div>
    </section>
  </section>
</template>

<style scoped>
.component-section {
  position: relative;
}
.content {
  position: relative;
  z-index: 10;
}
.logo_wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 28px;
}
.logo_icon {
  height: 25px;
  width: 25px;
  margin-right: 8px;
  padding-top: 4px;
}
.logo_header {
  color: var(--var-opposite-background-color);
  font-weight: 700;
  font-size: 28px;
}
.background-effect-1 {
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 0;
}
.background-effect-2 {
  position: absolute;
  bottom: 40px;
  width: 100%;
  z-index: 0;
}
.qr_wrap {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
.qr_code {
  padding: 16px;
  border-radius: 18px;
  background: var(--var-background-color);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}
.qr_placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.08);
}
.qr_placeholder_text {
  color: var(--var-opposite-background-color);
  font-size: 14px;
}
.description {
  margin: 28px 36px 0;
  text-align: center;
  color: var(--var-opposite-background-color);
  font-size: 16px;
  line-height: 22px;
}
.button_wrap {
  margin-top: 36px;
  display: flex;
  justify-content: center;
}
</style>
