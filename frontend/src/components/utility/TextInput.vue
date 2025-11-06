<template>
  <div>
    <span class="input_title"
      >{{ title }} <RequiredField font_size="20" v-if="editing && required"
    /></span>
    <div class="input_area">
      <span v-if="!editing"> {{ model }}</span>
      <div v-else>
        <div v-if="input_type === 'string'">
          <CellGroup inset class="input_area_editing">
            <Field
              v-model="model"
              type="textarea"
              placeholder="Заполни меня!"
              :rows="rows"
              autosize
              :maxlength="max_len"
            />
          </CellGroup>
        </div>
        <div v-if="input_type === 'date'">
          <input class="input_date" type="date" v-model="model" />
        </div>

        <!-- :TODO: awful abstraction -->
        <div class="gender_input" v-if="input_type === 'gender'">
          <RadioGroup v-model="model" direction="horizontal">
            <Radio name="F">Девушка</Radio>
            <Radio name="M">Парень</Radio>
          </RadioGroup>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Field, CellGroup, RadioGroup, Radio } from 'vant'
import RequiredField from '@/components/utility/RequiredField.vue'

const {
  title,
  editing = false,
  max_len = 20,
  rows = 1,
  input_type = 'string',
  required = false,
} = defineProps<{
  title: string
  editing?: boolean
  max_len?: number
  input_type?: string
  rows?: number
  required?: boolean
}>()

const model = defineModel<string>()
</script>

<style scoped>
.input_title {
  color: var(--var-secondary-emph-color);
  font-weight: 600;
  font-size: 20px;
}
.input_area {
  color: var(--var-opposite-background-color);
  margin-top: 10px;
  font-size: 15px !important;
  font-weight: 400 !important;
}
.input_area_editing {
  --van-cell-group-background: transparent;
  --van-cell-group-inset-padding: 0;
  --van-cell-background: var(--var-background-color);
  --van-field-input-text-color: var(--var-opposite-background-color);
  --van-cell-vertical-padding: 5px;
  --van-cell-horizontal-padding: 8px;
  border: 1px solid var(--var-primary-emph-color);
  border-radius: 10px;
  width: 180px;
}
.input_date {
  background: var(--var-background-color);
  border-radius: 10px;
  border: 1px solid var(--var-primary-emph-color);
  width: 176px;
  padding: 7px;
}

.gender_input {
  --van-radio-border-color: var(--var-primary-emph-color);
  --van-radio-label-color: var(--var-opposite-background-color);
  --van-radio-checked-icon-color: var(--var-primary-emph-color);
}
</style>
