window.mailjobs_active = window.mailjobs_active || function(initialEntries) {
    // Actual data
    var dataRows = JSON.parse(initialEntries),
        dataUpdated = true;

    // Handles the data source and how it's updated and sorted
    var dataStore = {
        data: function() {
            return {
                entries: [],
                paginate: true,
                filterable: true,
                sortable: true,
                can_resize: true,
                filter: '',
                sort_by: 3,
                sort_dir: 'dsc',
                page: 1,
                page_size: 10,
                page_size_old: 10,
                table: null,
                total_count: 0
            }
        },
        computed: {
            filtered_rows: function() {
                return this.entries;
            },
            sorted_rows: function() {
                return this.entries;
            },
            last_page: function() {
                return 1
            },
            visible_rows: function() {
                // Only trigger table update if data is marked as updated
                if (dataUpdated) {
                    this.getRows();
                    dataUpdated = false;
                }

                return this.entries;
            }
        },
        methods: {
            sortBy: function(column_id) {
                if(this.sort_by === column_id) {
                    // Change the direction if attempting to sort by the same column
                    this.sort_dir = (this.sort_dir === 'dsc') ? 'asc' : 'dsc';
                }
                else {
                    // Otherwise, reset the sort direction to the default one
                    this.sort_by = column_id;
                    this.sort_dir = (this.sort_by === 3) ? 'asc' : 'dsc'; // created_at defaults to descending
                }

                this.getRows();
            },
            setPage: function(pageNumber, event) {
                // Nothing to do
            },
            setTable: function(table) {
                this.table = table;
            },
            setFilterable: function(value) {
                this.filterable = false; // No filtering at the moment please
            },
            setPaginate: function(value) {
                this.paginate = false;
            },
            setSortable: function(value) {
                this.sortable = value;
            },
            setData: function(data) {
                this.getRows();
            },
            getRows: function() {
                var _this = this,
                    columns = ['destination', 'status', 'retry_count', 'created_at'];

                this.entries = dataRows;
                this.entries.sort(function(a, b) {
                    var column = columns[_this.sort_by] || 'created_at';
                    var compareValue = (a.fields[column] > b.fields[column]) ? 1 : -1;
                    var direction = _this.sort_dir == 'asc' ? 1 : -1;

                    return compareValue * direction;
                });
            }
        },
        watch: {
            filter: function() {
                this.page = 1;
            },
            page_size: function() {
                this.page = 1;
            }
        }
    };

    // Task revoking button component
    Vue.component('mailjobs-revoke-button', {
        template: `<button :disabled="row.fields.status == 'success' || row.fields.status == 'failed'" 
            @click="revokeTask">Revoke</button>'`,
        props: ['row'],
        methods: {
            revokeTask: function() {
                mailJobsSocket.send('{"action": "revoke_task", "job_pk":"' + this.row.pk + '"}');
            }
        }
    });

    // VueJS model
    var vm = new Vue({
        el: '#mail-jobs',
        data: {
            columns: [
                {label: 'Destination', field: 'fields.destination'},
                {label: 'Status', field: 'fields.status'},
                {label: 'Retries', field: 'fields.retry_count'},
                {label: 'Created', callback: function(row) {
                    var d = new Date(row.fields.created_at);
                    return ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth()+1)).slice(-2) + '/' +
                        d.getFullYear() + ' ' + ('0' + d.getHours()).slice(-2) + ':' +
                        ('0' + d.getMinutes()).slice(-2) + ':' + ('0' + d.getSeconds()).slice(-2);
                }},
                {label: 'Revoke', component: 'mailjobs-revoke-button'}
            ],
            dataStore: dataStore
        }
    });

    // List of job status that don't need to be tracked
    var discardStatus = {
        'success': true,
        'failed': true,
        'revoked': true
    };

    // Mail jobs socket
    // How to check if user is really a staff and can access this data??
    var mailJobsSocket = new WebSocket('ws://' + window.location.host + '/mailjobs/');
    mailJobsSocket.onmessage = function(e) {
        // Received new message from the server

        var message = JSON.parse(e.data);
        // console.log('incoming', message);

        switch (message.action) {
        case 'changed_status':
        case 'created':
            for (var i in message.jobs) {
                var job = message.jobs[i],
                    rowUpdated = false;

                // If there's an existing job with the same Primary Key
                //  updated it
                for (var j in dataRows) {
                    var row = dataRows[j];
                    if (row.pk != job.pk) continue;

                    // Update row status and retry count
                    var status = job.fields.status;
                    row.fields.status = status;
                    row.fields.retry_count = job.fields.retry_count;

                    // If success or failed, remove task from data rows
                    if (discardStatus[status]) {
                        setTimeout(function() {
                            // We'd have to look for it all over again
                            // Since the dataRows might have been sorted
                            for (var k in dataRows) {
                                if (row.pk != job.pk) continue;

                                dataRows.splice(k, 1);
                                break;
                            }
                        }, 1000);
                    }

                    rowUpdated = true;
                    break;
                }

                // Otherwise, add it as a new row
                if (!rowUpdated) dataRows.push(job);

                // Mark data as updated to trigger the table update
                dataUpdated = true;
            }
            break;
        default:
            break; 
        }
    }
}