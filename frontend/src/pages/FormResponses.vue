<template>
<q-page class="fit column justify-center items-center content-center">
  <q-btn
    label="Back to Form Browser"
    icon="arrow_back"
    class="q-my-xl"
    color="primary"
    :to="{ name: 'FormBrowser' }"
    />
  
  <q-card>
    <q-card-section>
      <div class="text-h6">{{ formInfo.title }}</div>
    </q-card-section>
    
    <q-tabs v-model="currentTab" class="text-primary">
      <q-tab label="By submission" name="submission" />
      <q-tab label="By question" name="question" />
    </q-tabs>
    
    <q-separator />
    
    <q-tab-panels v-model="currentTab" animated>
      <q-tab-panel name="submission">
	<q-table
	  flat
	  :rows="rawResponses"
	  :columns="columnsSubmission"
	  :pagination="submissionPagination"
	  row-key="id"
	  >
	  <template #header="props">
	    <q-tr :props="props">
	      <q-th auto-width />
              <q-th
		v-for="col in props.cols"
		:key="col.name"
		:props="props"
		>
		{{ col.label }}
              </q-th>
	    </q-tr>
	  </template>

	  <template #body="props">
	    <q-tr :props="props">
	      <q-td auto-width>
		<q-btn
		  @click="props.expand = !props.expand"
		  color="primary"
		  :icon="props.expand ? 'expand_less' : 'expand_more'"
		  size="sm"
		  round
		  dense
		  />
	      </q-td>
              <q-td
		v-for="col in props.cols"
		:key="col.name"
		:props="props"
		>
		{{ col.value }}
              </q-td>
	    </q-tr>
	    <q-tr v-show="props.expand" :props="props">
              <q-td colspan="100%">
		<q-list>
		  <q-item
		    v-for="value, key in props.row"
		    :key="key"
		    >
		    <q-item-section>
		      <div class="flex">
			<q-chip :label="key" color="primary" text-color="white" />
			<div>{{ value }}</div>
		      </div>
		    </q-item-section>
		  </q-item>
		</q-list>
              </q-td>
	    </q-tr>
	  </template>
	</q-table>
      </q-tab-panel>
      
      <q-tab-panel name="question">
        With so much content to display at once, and often so little screen real-estate,
        Cards have fast become the design pattern of choice for many companies, including
        the likes of Google and Twitter.
      </q-tab-panel>
    </q-tab-panels>
  </q-card>
  <q-table
    class="q-my-lg"
    :title="formInfo.title"
    :rows="listingType === 'submission' ? rawResponses : questions"
    :columns="listingType === 'submission' ? columnsSubmission : columnsQuestion"
    :pagination="pagination"
    row-key="id"
    >
    <template #top-right>
      <q-btn-toggle
        v-model="listingType"
        class="q-mx-md"
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
    </template>
    <template #header="props">
      <q-tr :props="props">
	<q-th auto-width />
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>

    <template #body="props">
      <q-tr :props="props">
	<q-td auto-width>
          <q-btn
            @click="props.expand = !props.expand"
            color="primary"
            :icon="props.expand ? 'expand_less' : 'expand_more'"
            size="sm"
            round
            dense
            />
	</q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          >
          {{ col.value }}
        </q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
	  <q-markup-table flat v-if="listingType === 'submission'">
	    <thead>
	    </thead>
	    <tbody>
	      <tr v-for="value, key in props.row.response" :key="key">
		<td class="text-weight-bold text-left">
		  {{ key }}
		</td>
		<td>
		  {{ value }}
		</td>
	      </tr>
	    </tbody>
	  </q-markup-table>
	  <q-markup-table flat v-else>
	    <thead>
	    </thead>
	    <tbody>
	      <tr v-for="value, i in props.row.responses" :key="i">
		<td>
		  {{ value }}
		</td>
	      </tr>
	    </tbody>
	  </q-markup-table>
        </q-td>
      </q-tr>
    </template>
  </q-table>

  <q-card class="my-card" flat bordered>
      <q-card-section>
	<q-checkbox v-model="showJson" label="Show JSON" />
      </q-card-section>
      <q-slide-transition>
        <div v-show="showJson">
          <q-separator />
          <q-card-section class="text-subtitle2">
	    
          </q-card-section>
        </div>
      </q-slide-transition>
    </q-card>
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
    questions: {
      get () {
        let outData = [];
	let tmpData = {};
	for (let entry of this.rawResponses) {
	  for (let key in entry.response) {
	    if (!entry.response[key].length)
	      continue
	    if (key in tmpData) {
	      tmpData[key].push(entry.response[key]);
	    }
	    else {
	      tmpData[key] = [entry.response[key]];
	    }
	  }
	}
	for (let key in tmpData)
	  outData.push({id: key, responses: tmpData[key], count: tmpData[key].length})
	return outData;
      }
    },
  },

  data () {
    return {
      formInfo: {},
      currentTab: "submission",
      submissionPagination: {
        rowsPerPage: 10
      },
      pagination: {
        rowsPerPage: 10
      },
      columnsSubmission: [
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          required: true,
          sortable: true
        },
        {
          name: 'timestamp',
          label: 'Timestamp',
          field: 'timestamp',
          required: true,
          sortable: true
        },
      ],
      columnsQuestion: [
        {
          name: 'question',
          label: 'Question',
          field: 'id',
          required: true,
          sortable: true
        },
	{
          name: 'responseCount',
          label: 'Response Count',
          field: 'count',
          required: true,
          sortable: true
        },

      ],
      filter: '',
      rawResponses: [],
      responsesLoading: false,
      infoLoading: false,
      showJson: false,
      responsesError: false,
      infoError: false,
      listingType: 'submission'
    }
  },

  methods: {
    getEntry () {
      this.responsesLoading = true;
      this.responsesError = false;
      axios
	.get('/api/v1/form/' + this.identifier + '/responses')
        .then((response) => this.rawResponses = response.data.responses)
	.catch(() => this.responsesError = true)
	.finally(() => this.responsesLoading = false);
      this.infoLoading = true;
      this.infoError = false;
      axios
	.get('/api/v1/form/' + this.identifier)
        .then((response) => this.formInfo = response.data.form)
	.catch((err) => this.infoError = true)
      	.finally(() => this.infoLoading = false);
    },
  },

  mounted () {
    this.getEntry()
  }
})
</script>
