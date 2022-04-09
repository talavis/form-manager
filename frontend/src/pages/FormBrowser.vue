<template>
<q-page class="flex flex-center">
  <q-card flat>
    <q-card-section>
  <q-table
    title="Available forms"
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
          name: 'identifier',
          label: 'Identifier',
          field: 'identifier',
          required: true,
          align: 'left',
          sortable: true,
        },
        {
          name: 'title',
          label: 'Title',
          field: 'title',
          required: true,
          sortable: true
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
      this.$router.push({name: 'FormBrowser', form: row.identifier});
    }
  },

  mounted () {
    this.getEntries();
  }
})
</script>
