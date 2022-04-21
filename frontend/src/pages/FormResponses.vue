<template>
<q-page class="fit column justify-center items-center content-center">
  <q-btn
    label="Back to Form Browser"
    icon="arrow_back"
    class="q-my-lg"
    color="primary"
    :to="{ name: 'FormBrowser' }"
    />

  <q-card v-if="Object.keys(urlInfo).length > 0" class="q-my-sm">
    <q-card-section>
      &lt;form action="{{ urlInfo.submission_url }}" method="{{ urlInfo.method }}"&gt;
    </q-card-section>
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


  <q-btn
    label="Copy JSON to clipboard"
    icon="content_copy"
    class="q-my-lg"
    color="secondary"
    @click="jsonToClipboard(listingType === 'submission' ? rawResponses : questions)"
    />
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'
import { copyToClipboard } from 'quasar'

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
      rawResponses: [],
      responsesLoading: false,
      responsesError: false,
      infoLoading: false,
      infoError: false,
      urlLoading: false,
      urlError: false,
      urlInfo: {},
      listingType: 'submission',
      showCopyInfo: false,
    }
  },

  methods: {
    jsonToClipboard (responseData) {
      copyToClipboard(JSON.stringify(responseData))
	.then(() => {
	  // success!
	})
	.catch(() => {
	  // fail
	})
      this.$q.notify({
        group: false,
        message: 'JSON copied to clipboard.',
        color: 'primary'
      })
    },
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
      this.urlLoading = true;
      this.urlError = false;
      axios
	.get('/api/v1/form/' + this.identifier + '/url')
        .then((response) => this.urlInfo = response.data)
	.catch((err) => this.urlError = true)
      	.finally(() => this.urlLoading = false);
    },
  },

  mounted () {
    this.getEntry()
  }
})
</script>
