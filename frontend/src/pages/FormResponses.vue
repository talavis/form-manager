<template>
<q-page class="flex flex-center">
  <div>
    <span class="text-h3 text-primary">
      Form Responses for {{ identifier }}
    </span>
    <div>
      <q-btn-toggle
        v-model="listingType"
        class="my-custom-toggle"
        no-caps
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
		  {label: 'By submission', value: 'submission'},
		  {label: 'By question', value: 'question'}
		  ]"
	/>
    </div>
    <q-list v-if="listingType === 'submission'">
      <q-expansion-item
	v-for="entry, i in responses"
	:key="i"
	:label="(i+1).toString()"
	>
	<q-item-section>
	  <q-list>
	    <q-item
	      v-for="item, key in entry"
	      :key="key"
	      >
	      <q-item-section>
		<div><span class="text-weight-bold">{{ key }}: </span> {{ item }}</div>
	      </q-item-section>
	    </q-item>
	  </q-list>
	</q-item-section>
      </q-expansion-item>
    </q-list>
    <q-list v-else>
      <q-expansion-item
	v-for="item, key in responses"
	:key="key"
	:label="key"
	>
	<q-item-section>
	  <q-list>
	    <q-item
	      v-for="entry, i in item"
	      :key="i"
	      >
	      <q-item-section>
		{{ entry }}
	      </q-item-section>
	    </q-item>
	  </q-list>
	</q-item-section>
      </q-expansion-item>
    </q-list>
    <q-card class="my-card" flat bordered>
      <q-card-section>
	<q-checkbox v-model="showJson" label="Show JSON" />
      </q-card-section>
      <q-slide-transition>
        <div v-show="showJson">
          <q-separator />
          <q-card-section class="text-subitle2">
            {{ responses }}
          </q-card-section>
        </div>
      </q-slide-transition>
    </q-card>
  </div>
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'FormResponses',
  props: {
    identifier: {
      type: String,
      required: true,
    }
  },

  computed: {
    responses: {
      get () {
	let outData
	if (this.rawResponses.length === 0)
	  return []
	if (this.listingType === 'submission') {
	  outData = this.rawResponses.map(
	    function (entry) {
	      let tmp = entry.response;
	      tmp.timestamp = entry.timestamp;
	      return tmp
	    }
	  )
	}
	else if (this.listingType === 'question') {
	  outData = {};
	  console.log(Object.keys(this.rawResponses[0]))
	  console.log(Object.keys(this.rawResponses[0]['response']))
	  for (let entry of this.rawResponses) {
	    for (let key in entry.response) {
	      console.log(key)
	      if (key in outData) {
		outData[key].push(entry.response[key]);
	      }
	      else {
		outData[key] = [entry.response[key]];
	      }
	    }
	  }
	}
	return outData;
      },
    },
  },

  data () {
    return {
      rawResponses: [],
      showJson: false,
      listingType: 'submission'
    }
  },

  methods: {
    getEntry () {
      axios
	.get('/api/v1/form/' + this.identifier + '/responses')
        .then((response) => {
	  this.rawResponses = response.data['responses']
	})
      .catch((err) => {
	this.error = true;
      });
    },
  },

  mounted () {
    this.getEntry()
  }
})
</script>
