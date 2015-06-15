# encoding: utf-8

from config import memc
from django.http import HttpResponse

def mol_result(request):
    """
	MOL Payment Callback
    """
    data = dict(request.REQUEST.iteritems())
    logging.info("mol_result: %s"%str(data))
    referenceId = data.get("referenceId")
    mol = MOL.get(referenceId)
    if not mol:
        return HttpResponse("failed")

    # check the sign
    if not mol.check_sign(data):
        return HttpResponse("failed")

    paymentStatusCode = data.get("paymentStatusCode")
    if paymentStatusCode != "00":
        mol.update_order(data)

        # query order details
        #mol.query_order(data)
        return HttpResponse("failed")
    
    result = mol.update_order(data)
    return HttpResponse("success" if result else "failed")
