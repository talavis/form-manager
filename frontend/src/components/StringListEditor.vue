<template>
<div>
  <div>
    <q-input
      dense
      stack-label
      hide-bottom-space
      outlined
      :label="fieldTitle"
      v-model="newValue"
      @keyup.enter="addValue"
      :rules="[ function (val) { return (evaluateValue(val) || val.length === 0) || 'No whitespace at beginning nor end and must not already exist.' }]">
      <template #after>
        <q-btn
	  icon="add"
          dense
          size="md"
          :disabled="!enableAdd"
          color="positive"
          @click="addValue" />
      </template>
    </q-input>
    <div class="flex">
      <q-chip
	v-for="value of entries"
	:key="value"
	square
	removable
	color="primary"
	text-color="white"
	@remove="deleteValue(value)">
	{{ value }}
      </q-chip>
    </div>
  </div>
  <q-inner-loading :showing="isLoading">
    <q-spinner-gears size="100px" color="primary" />
  </q-inner-loading>
</div>
</template>

<script>
import { useUserStore } from 'stores/user'

export default {
  name: 'StringListEditor',

  computed: {
    enableAdd: {
      get () {
        return this.evaluateValue(this.newValue);
      },
    },
    entries: {
      get () {
	if (this.hideCurrentUser) {
	  const store = useUserStore();
	  return this.modelValue.filter((entry) => entry !== store.email)
	}
	else return this.modelValue;
      }
    }
  },
  
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },

    hideCurrentUser: {
      type: Boolean,
      default: false,
    },

    modelValue: {
      type: Array,
      required: true,
    },

    fieldTitle: {
      type: String,
      required: true,
    },

    fieldIcon: {
      type: String,
      default: 'label',
    },
  },

  data () {
    return {
      newValue: '',
      valueExistsError: false,
    }
  },

  emits: ['update:modelValue'],
  methods: {
    evaluateValue (val) {
      return (val.trim() === val && !this.modelValue.includes(this.newValue));
    },

    addValue() {
      if (this.enableAdd) {
        this.valueExistsError = false;
        if (!this.modelValue.includes(this.newValue)) {
          this.$emit('update:modelValue', this.modelValue.concat(this.newValue))
          this.newValue = '';
        }
        else
          this.valueExistsError = true;
      }
    },

    deleteValue(value) {
      this.$emit('update:modelValue', this.modelValue.filter((entry) => entry !== value))
    },
  },
}
</script>
