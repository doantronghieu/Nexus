module.exports = {
	apps: [
		{
			name: "NuxtJS",
			exec_mode: "cluster",
			instances: "max",
			script: ".output/server/index.mjs",
			env: {
				PORT: 3000,
				NODE_ENV: "production",
			},
		},
	],
};
