odoo.define('bi_credit_limit_on_pos.ClientListScreenWidget', function(require) {
	"use strict";

	const PartnerListScreen = require('point_of_sale.PartnerListScreen');
	const Registries = require('point_of_sale.Registries');

	const PartnerListScreenWidget = (PartnerListScreen) =>
		class extends PartnerListScreen {
			setup() {
				super.setup();
				var self = this;
				setInterval(function(){
					self.searchPartner();
				}, 5000);
				this.searchPartner()
			}
	};

	Registries.Component.extend(PartnerListScreen, PartnerListScreenWidget);

	return PartnerListScreen;

});
