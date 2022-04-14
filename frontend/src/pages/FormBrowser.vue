<template>
<q-page class="flex flex-center">
  <q-card flat>
    <q-card-section>
  <q-table
    title="Forms"
    :rows="entries"
    :columns="columns"
    row-key="id"
    :pagination="pagination"
    :filter="filter"
    :loading="loading"
    no-data-label="No entries found"
    :no-results-label="filter + ' does not match any entries'"
    @row-click="gotoEntry"
    >
    <template v-slot:top-right>
      <q-input rounded outlined dense debounce="300" v-model="filter" placeholder="Search">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </template>
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td key="title" :props="props">
          {{ props.row.title }}
        </q-td>
        <q-td key="identifier" :props="props">
          {{ props.row.identifier }}
        </q-td>
        <q-td key="recaptcha" :props="props">
          <q-icon
	    :name="props.row.recaptcha ? 'check_circle' : 'cancel'"
	    :color="props.row.recaptcha ? 'positive' : 'negative'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="sendEmail" :props="props">
          <q-icon
	    :name="props.row.email ? 'check_circle' : 'cancel'"
	    :color="props.row.email ? 'primary' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
          <div class="text-left">This is expand slot for row above: {{ props.row.name }}.</div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
  </q-card-section>
    <q-card-section>
      <q-btn icon="add" @click="addDialogOpen = true"/>
      </q-card-section>
  </q-card>
  <form-edit-dialog v-model="addDialogOpen" />
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import EditFormInfo from 'components/EditFormInfo.vue'
import axios from 'axios'

export default defineComponent({
  name: 'FormBrowser',
  components: {
    'form-edit-dialog': EditFormInfo
  },
  data () {
    return {
      entries: [],
      filter: '',
      addDialogOpen: false,
      pageAbout: '',
      pageNew: '',
      loading: false,
      pagination: {
        rowsPerPage: 20
      },
      columns: [
        {
          name: 'title',
          label: 'Title',
          field: 'title',
          required: true,
	  align: 'left',
          sortable: true
        },
        {
          name: 'identifier',
          label: 'Identifier',
          field: 'identifier',
          required: true,
          sortable: true,
        },
        {
          name: 'recaptcha',
          label: 'reCAPTCHA',
          field: 'recaptcha',
          required: true,
          sortable: true,
        },
        {
          name: 'sendEmail',
          label: 'Send email',
          field: 'email',
          required: true,
          sortable: true,
        },
      ]
    }
  },
  methods: {
    getEntries () {
      axios
	.get('/api/v1/form')
        .then((response) => {
	  this.entries = response.data['forms']
	})
      .catch((err) => {
	this.error = true;
      });
    },
    gotoEntry(evt, row, index) {
      this.$router.push({name: 'FormResponses', params: {identifier: row.identifier}});
    }
  },

  mounted () {
    this.getEntries();
  }
})
</script>
