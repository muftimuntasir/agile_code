odoo.define('bi_credit_limit_on_pos.PaymentScreenWidget', function(require){
	'use strict';

	const PaymentScreen = require('point_of_sale.PaymentScreen');
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { Component } = owl;
	var rpc = require('web.rpc');

	const PaymentScreenWidget = (PaymentScreen) =>
		class extends PaymentScreen {
			setup() {
                super.setup();
			}

			async validateOrder(isForceValidate) {
                var self = this;
                var currentOrder = this.env.pos.get_order();
                var plines = currentOrder.get_paymentlines();
                var selected_lines = this.env.pos.get_order().selected_paymentline;
                var partner = currentOrder.get_partner();
                var a = [];
                var total_crdt = 0;

                for(var i = 0; i < plines.length; i++) {
                    if(plines[i].payment_method.is_credit == true){
                        total_crdt += plines[i].amount;
                        a.push(plines[i]);
                    }
                }

                if(currentOrder.get_orderlines().length === 0){
                    self.showPopup('ErrorPopup',{
                        'title': this.env._t('Empty Order'),
                        'body': this.env._t('There must be at least one product in your order before it can be validated.'),
                    });
                    return;
                }

                else if (total_crdt > 0  && !currentOrder.get_partner()){
                    self.showPopup('ErrorPopup',{
                        'title': this.env._t('Unknown customer'),
                        'body': this.env._t('Select customer first.'),
                    });
                    return;
                }

                else if (total_crdt > 0  && currentOrder.is_to_invoice()){
                    self.showPopup('ErrorPopup',{
                        'title': this.env._t('Not Allowed'),
                        'body': this.env._t('Create Inovice is not allowed for Credit Payments.'),
                    });
                    currentOrder.set_to_invoice(false);
                    return;
                }

                else if (partner){
                    if(total_crdt > 0 && partner.active_credit_limit == false){
                        self.showPopup('ErrorPopup',{
                            'title': this.env._t('Not Allowed'),
                            'body': this.env._t('Selected customer is not allowed to use credit payment.'),
                        });
                        return;
                    }
                    else if(partner.blocking_amount !== 0 && partner.active_credit_limit){
                        let will_be_amt = partner.custom_credit + total_crdt;
                        if (total_crdt > 0 ) {
                            if(currentOrder.get_change() > 0){
                                   self.showPopup('ErrorPopup',{
                                    'title': this.env._t('Payment Amount Exceeded'),
                                    'body': this.env._t('You cannot Pay More than Total Amount'),
                                });
                                return;
                            }
                            else if(will_be_amt >= partner.blocking_amount){
                                await self.showPopup('BiWarningBlockingPopup',{
                                    'title': self.env._t('Credit Limit Exceeding'),
                                    'custom_credit': partner.custom_credit,
                                    'blocking_amount': partner.blocking_amount,
                                    'available_credit': partner.available_credit,
                                });
                                self.showScreen('PaymentScreen');
                                return;
                            }
                            else if(will_be_amt >= partner.warning_amount){
                                const { confirmed, payload } = await self.showPopup('BiWarningPopup',{
                                    'body': self.env._t('The credit warning is exceeding the limit.'),
                                    'custom_credit': partner.custom_credit,
                                    'blocking_amount': partner.blocking_amount,
                                    'available_credit': partner.available_credit,
                                });
                                if (confirmed) {
                                    super.validateOrder(...arguments);
                                }
                            }
                            else{
                                super.validateOrder(...arguments);
                            }
                        }else{
                            super.validateOrder(...arguments);
                        }
                    }
                    else{
                        super.validateOrder(...arguments);
                    }
                }else{
                    super.validateOrder(...arguments);
                }
            }
	};

	Registries.Component.extend(PaymentScreen, PaymentScreenWidget);
	return PaymentScreen;

});
