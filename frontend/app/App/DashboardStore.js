var Reflux = require("reflux");

module.exports = Reflux.createStore({
	init: function() {
		this._data = {
            budget: [
                [ 'Budget', 12 ],
                [ 'Actual', 53 ]
            ],
            planning: [
                [ 'Planned', 22 ],
                [ 'Actual', 34 ]
            ],
            implementation: [
                [ 'Planned', 24 ],
                [ 'Actual', 30 ]
            ],
        };
	},

	getData: function() {
		return this._data;
	}
});
