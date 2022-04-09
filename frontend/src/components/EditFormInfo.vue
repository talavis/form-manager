<template>
<q-dialog
  :model-value="modelValue"
  @update:model-value="updateVisibility"
  >
  <q-card style="width: 400em">
    <q-card-section>
      <q-list>
        <q-item-label caption>User Data</q-item-label>
        <q-item>
          <q-item-section>
            <q-input
	      outlined
              label="Title"
              v-model="formData.title"
	      />
          </q-item-section>
        </q-item>
        <q-item>
          <q-item-section>
            <q-input
	      outlined
              label="Identifier"
              v-model="formData.identifier"/>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card-section>

    <q-card-actions align="left">
      <q-btn
	label="Save"
        color="positive"
        type="submit"
        @click="saveForm"
        :loading="saveWaiting"/>
      <q-btn
	label="Cancel"
        color="grey-6"
        v-close-popup />
    </q-card-actions>
    <q-card-actions align="right">
      <span v-show="saveError" class="text-negative">Save failed</span>
    </q-card-actions>
  </q-card>
</q-dialog>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'EditFormInfo',
  
  props: {
    modelValue: {
      // visibility for v-model
      type: Boolean,
      required: true,
    }
  },
  
  emits: ['update:modelValue'],
  
  data () {
    return {
      formData: {
	title: '',
	identifier: '',
      },
      saveError: false,
      saveWaiting: false,
    }
  },
  
  methods: {
    updateVisibility (value) {
      this.$emit('update:modelValue', value)
    },

    saveForm () {
      this.saveError = false;
      this.saveWaiting = true;
      axios
	.post('/api/v1/form', this.formData)
        .then((response) => {
	  this.updateVisibility(false);;
      })
      .catch((err) => {
	this.saveError = true;
      });
    },
  }
})
</script>
