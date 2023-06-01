odoo.define('bi_credit_limit_on_pos.BiWarningBlockingPopup', function(require) {
	'use strict';

	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	const Registries = require('point_of_sale.Registries');


	class BiWarningBlockingPopup extends AbstractAwaitablePopup {
		setup() {
            super.setup();
		}
	}
	BiWarningBlockingPopup.template = 'BiWarningBlockingPopup';
	Registries.Component.add(BiWarningBlockingPopup);

	return BiWarningBlockingPopup;
});
