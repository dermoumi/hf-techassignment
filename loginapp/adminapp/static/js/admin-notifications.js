window.adminNotifications = window.adminNotifications || function(api_url) {
    // Helper function to get a cookie
    // Needed to get the csrf token for Django's ajax requests
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

    // Data
    var notificationEntries = [];

    // Notifications component
    Vue.component('notifications', {
        props: ['notificationCount'],
        template: '#notifications-script',
        data: function() {
            return {
                windowOpen: false,
                initialized: false,
                entries: notificationEntries
            };
        },
        methods: {
            toggleWindow: function() {
                this.windowOpen = !this.windowOpen;

                // If the window was opened
                if (this.windowOpen) {
                    // Mark all notifications as read
                    mailJobsSocket.send('{"action": "notification_all_read"}');

                    // If it's the first time, load notifications from server using an ajax request
                    if (!this.initialized) {
                        var r = new XMLHttpRequest();
                        r.open("POST", api_url, true);
                        r.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                        r.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                        r.onreadystatechange = function () {
                            if (r.readyState != 4 || r.status != 200) return;

                            var output = JSON.parse(r.responseText);
                            notificationEntries = output;
                            this.entries = notificationEntries;
                        }.bind(this);
                        r.send();

                        this.initialized = true;
                    }
                } 
            }
        }
    });

    // VueJS model
    var vm = new Vue({
        el: '#header',
        data: {
            notificationCount: 0
        }
    })

    // Admin notifications socket
    var mailJobsSocket = new WebSocket('ws://' + window.location.host + '/admin/');
    mailJobsSocket.onmessage = function(e) {
        // Received new message from the server
        var message = JSON.parse(e.data);
        console.log('incoming', message);

        switch (message.action) {
        case 'reply_channel':
            vm.notificationCount = message.unread_notification_count;
            break;
        case 'notification':
            vm.notificationCount += message.notifications.length;
            for (var i in message.notifications) {
                var notif = message.notifications[i];
                notificationEntries.unshift({
                    fields: {
                        unread: true,
                        notification: {
                            kind: notif.fields.kind,
                            link: notif.fields.link,
                            content: notif.fields.content
                        }
                    }
                });
            }
            break;
        case 'notification_read':
            // TODO: Implement notification read action in front-end
            break;
        case 'notification_all_read':
            vm.notificationCount = 0;
            for (var i in notificationEntries) {
                notificationEntries[i].fields.unread = false;
            }
            break;
        default:
            break; 
        }
    }
};
