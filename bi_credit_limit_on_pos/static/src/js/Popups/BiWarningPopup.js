odoo.define('bi_credit_limit_on_pos.BiWarningPopup', function(require) {
	'use strict';

	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	const Registries = require('point_of_sale.Registries');


	class BiWarningPopup extends AbstractAwaitablePopup {
		setup() {
            super.setup();
		}
	}
	BiWarningPopup.template = 'BiWarningPopup';
	Registries.Component.add(BiWarningPopup);

	return BiWarningPopup;
});
