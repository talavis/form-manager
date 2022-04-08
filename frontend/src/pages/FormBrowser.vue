<template>
<q-page class="flex flex-center">
  <q-table
    :rows="entries"
    :columns="columns"
    row-key="id"
    :pagination="pagination"
    :filter="filter"
    :loading="loading"
    no-data-label="No entries found"
    :no-results-label="filter + ' does not match any entries'"
    />

</q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'FormBrowser',
  data () {
    return {
      entries: [{identifier: 'id1', title: 'Title 1'}],
      filter: '',
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

})
</script>
