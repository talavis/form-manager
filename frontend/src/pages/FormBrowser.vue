<template>
<q-page class="flex flex-center">
  <q-table
    title="Forms"
    :rows="entries"
    :columns="columns"
    row-key="identifier"
    :pagination="pagination"
    :filter="filter"
    :loading="loading"
    no-data-label="No entries found"
    :no-results-label="filter + ' does not match any entries'"
    >
    <template #top-right>
      <q-btn
	class="q-mx-sm"
	dense
	round
	outline
	icon="add"
	@click="addForm" />      
      <q-input rounded outlined dense debounce="300" v-model="filter" placeholder="Search">
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
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
	<q-th auto-width />
      </q-tr>
    </template>
    <template #body="props">
      <q-tr :props="props">
	<q-td auto-width>
          <q-btn
            @click="expandItem(props)"
            color="primary"
            :icon="props.expand ? 'expand_less' : 'expand_more'"
            size="sm"
            round
            dense
            />
	</q-td>
        <q-td key="title" :props="props">
          {{ props.row.title }}
        </q-td>
        <q-td key="identifier" :props="props">
          {{ props.row.identifier }}
        </q-td>
        <q-td key="recaptcha" :props="props">
          <q-icon
	    :name="props.row.recaptcha_secret.length ? 'check_circle' : 'cancel'"
	    :color="props.row.recaptcha_secret.length ? 'positive' : 'negative'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="sendEmail" :props="props">
          <q-icon
	    :name="props.row.email.length ? 'check_circle' : 'cancel'"
	    :color="props.row.email.length ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
        <q-td key="redirect" :props="props">
          <q-icon
	    :name="props.row.redirect.length ? 'check_circle' : 'cancel'"
	    :color="props.row.redirect.length ? 'accent' : 'secondary'"
	    size="1.5em">
          </q-icon>
        </q-td>
	<q-td auto-width>
          <q-btn
            color="primary"
            icon="account_tree"
            size="sm"
            round
            dense
	    @click=gotoEntry(props.row.identifier)
            />
	</q-td>
      </q-tr>
      <q-tr v-if="props.expand" :props="props">
        <q-td colspan="100%">
	  <q-list dense>
            <q-item>
              <q-item-section>
		<q-input
		  dense
		  outlined
		  label="Title"
		  v-model="editData[props.key].title"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<q-input
		  dense
		  outlined
		  label="Redirect to"
		  v-model="editData[props.key].redirect"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<q-input
		  dense
		  outlined
		  label="Recaptcha secret"
		  v-model="editData[props.key].recaptcha_secret"
		  />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
		<q-input
		  dense
		  outlined
		  label="Email"
		  v-model="editData[props.key].email"
		  hint="Separate multiple emails with ;"
		  >
		</q-input>
              </q-item-section>
            </q-item>
	    <q-item>
	      <q-item-section>
		<div class="items-end">
		  <q-btn
		    flat
		    round
		    dense
		    size="md"
		    icon="check"
		    color="positive"
		    :loading="editData[props.key].saving"
		    @click="saveEdit(props)" />
		  <q-btn
		    flat
		    round
		    dense
		    bg-color="positive"
		    size="md"
		    icon="cancel"
		    color="negative"
		    @click="cancelEdit(props)" />
		  <q-btn
		    flat
		    round
		    dense
		    class="q-ml-md"
		    bg-color="positive"
		    size="md"
		    icon="delete"
		    color="negative"
		    @click="deleteForm(props)" />
		  <span v-show="editData[props.key].saveError" class="text-negative">Save failed</span>
		</div>
	      </q-item-section>
	    </q-item>
	  </q-list>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'FormBrowser',
  data () {
    return {
      entries: [],
      editData: {},
      filter: '',
      loading: false,
      loadError: false,
      saveError: false,
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
        {
          name: 'redirect',
          label: 'Redirect',
          field: 'redirect',
          required: true,
          sortable: true,
        },
      ]
    }
  },
  methods: {
    getEntries () {
      this.loading = true;
      axios
	.get('/api/v1/form')
        .then((response) => {
	  this.entries = response.data['forms']
	  for (let entry of this.entries) {
	    if (entry.email_recipients.length > 0)
	      entry.email = entry.email_recipients.join(';');
	    else
      entry.email = "";
	    delete entry.email_recipients;
	    
	  }
	})
      .catch((err) => {
	this.loadError = true;
      })
      .finally(() => this.loading = false);
    },
    gotoEntry(identifier) {
      this.$router.push({name: 'FormResponses', params: {identifier: identifier}});
    },
    deleteForm(entry) {
      axios
	.delete('/api/v1/form/' + entry.row.identifier)
        .then(() => {
	  entry.expand = false;
	  delete this.editData[entry.row.identifier];
	  this.getEntries();
	})
    },
    addForm() {
      axios
	.post('/api/v1/form', {}, {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then(() => this.getEntries())
    },
    expandItem(entry) {
      entry.expand = !entry.expand;
      if (!(entry.key in this.editData)) {
	this.editData[entry.key] = {
	  title: entry.row.title,
	  recaptcha_secret: entry.row.recaptcha_secret,
	  email: entry.row.email,
	  redirect: entry.row.redirect,
	  saving: false,
	  saveError: false,
	}
      }
    },
    saveEdit(entry) {
      this.saveError = false;
      this.editData[entry.key].saving = true;
      this.editData[entry.key].saveError = false;
      let outgoing = JSON.parse(JSON.stringify(this.editData[entry.key]));
      outgoing.email_recipients = outgoing.email.split(';');
      outgoing.email_recipients.forEach((entry, index) => outgoing.email_recipients[index] = entry.trim())
      delete outgoing.email;
      delete outgoing.saving;
      delete outgoing.saveError;
      axios
	.patch('/api/v1/form/' + entry.row.identifier, outgoing, {headers: {'X-CSRFToken': this.$q.cookies.get('_csrf_token')}})
        .then((response) => {
	  entry.expand = false;
	  delete this.editData[entry.key];
	  this.getEntries();
	  })
	.catch((err) => this.editData[entry.key].saveError = true)
	.finally(() => this.editData[entry.key].saving = false);
    },
    cancelEdit(entry) {
      entry.expand = false;
      delete this.editData[entry.key];
    },
  },

  mounted () {
    this.getEntries();
  }
})
</script>
