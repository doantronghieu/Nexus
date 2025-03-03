import { defineStore } from "pinia";

export const useNotificationsStore = defineStore("notifications", {
	state: () => ({
		notifications: [],
	}),
	actions: {
		show(notification) {
			const id = Date.now();
			this.notifications.push({
				id,
				type: notification.type || "info",
				message: notification.message,
				duration: notification.duration || 3000,
			});

			// Automatically remove the notification after duration
			setTimeout(() => {
				this.remove(id);
			}, notification.duration || 3000);
		},
		remove(id) {
			const index = this.notifications.findIndex((n) => n.id === id);
			if (index > -1) {
				this.notifications.splice(index, 1);
			}
		},
		success(message, duration = 3000) {
			this.show({ type: "success", message, duration });
		},
		error(message, duration = 3000) {
			this.show({ type: "error", message, duration });
		},
		info(message, duration = 3000) {
			this.show({ type: "info", message, duration });
		},
	},
});
