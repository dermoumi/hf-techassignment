window.mailjobs_all = window.mailjobs_all || function(api_url) {
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }

      return cookieValue;
    }

    var dataStore = {
      data: function() {
        return {
          entries: [],
          paginate: true,
          filterable: true,
          sortable: true,
          can_resize: true,
          filter: '',
          sort_by: 4,
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
          return Math.ceil(this.total_count / this.page_size);
        },

        visible_rows: function() {
          if (this.page_size !== this.page_size_old) {
            this.getRows(undefined, function() {
              this.page_size_old = this.page_size;
            }.bind(this));
          }

          return this.entries;
        }
      },

      methods: {
        sortBy: function(column_id) {
          var sort_dir = this.sort_dir;
          if(this.sort_by === column_id) {
            switch(sort_dir){
              case 'asc':
                sort_dir = 'dsc';
                break;
              default:
                sort_dir = 'asc';
                break;
            }
          }
          else {
            sort_dir = this.sort_by === 3 ? 'asc' : 'dsc'; // created_at defaults to descending
          }

          this.getRows({sort_by: column_id, sort_dir: sort_dir}, function() {
            this.sort_by = column_id;
            this.sort_dir = sort_dir;
          }.bind(this));
        },

        setPage: function(pageNumber, event) {
          this.getRows({page: pageNumber}, function() {
            this.page = pageNumber;
          }.bind(this));

          event.target.blur();
        },

        setTable: function(table) {
          this.table = table;
        },

        setFilterable: function(value) {
          this.filterable = false; // No filtering please
        },

        setPaginate: function(value) {
          this.paginate = value;
        },

        setSortable: function(value) {
          this.sortable = value;
        },

        setData: function(data) {
          this.getRows({}, function() {
            // Nothing to do?
          }.bind(this));
        },

        getRows: function(params, callback) {
            var columns = ['destination', 'status', 'retry_count', 'created_at'];

            params = params || {};
            params.sort_by = columns[params.sort_by || this.sort_by] || 'created_at';
            params.sort_dir = params.sort_dir || this.sort_dir || 'dsc';
            params.page = params.page || this.page;
            params.page_size = params.page_size || this.page_size;

            var r = new XMLHttpRequest();
            r.open("POST", api_url, true);
            r.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            r.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            r.onreadystatechange = function () {
              if (r.readyState != 4 || r.status != 200) return;

              var output = JSON.parse(r.responseText);
              this.entries = output.entries;
              this.total_count = output.total_count;

              callback && callback();
            }.bind(this);

            var paramsList = [];
            for (var key in params) {
              paramsList.push(key + '=' + params[key]);
            }
            r.send(paramsList.join('&'));
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

    var vm = new Vue({
      el: '#mail-jobs',
      data: {
        columns: [
          {label: 'Destination', field: 'fields.destination'},
          {label: 'Status', field: 'fields.status'},
          {label: 'Retries', field: 'fields.retry_count'},
          {label: 'Created', field: 'fields.created_at'},
        ],
        dataStore: dataStore
      }
    });
};