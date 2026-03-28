import stripe
from django.conf import settings
from rest_framework import status, views, permissions
from rest_framework.response import Response
from donations.models import Donation
from .models import Transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        donation_id = request.data.get('donation_id')
        try:
            donation = Donation.objects.get(id=donation_id)
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(donation.amount * 100),
                            'product_data': {
                                'name': f'Donation to {donation.campaign.title}',
                                'description': f'Donation from {donation.donor.username if donation.donor else "Guest"}',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/') + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/') + '?canceled=true',
            )
            
            # Create transaction record
            Transaction.objects.update_or_create(
                donation=donation,
                defaults={
                    'stripe_charge_id': checkout_session.id,
                    'verification_status': Transaction.Status.CREATED
                }
            )

            return Response({'id': checkout_session.id, 'url': checkout_session.url}, status=status.HTTP_200_OK)
            
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StripeWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        # TODO: Add Stripe Webhook Secret to settings and setup verification
        # For MVP, we will assume validity or skip webhook signature 
        # in favor of direct frontend session checks.
        
        import json
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event.type == 'checkout.session.completed':
            session = event.data.object
            
            # Fulfill the order
            try:
                transaction = Transaction.objects.get(stripe_charge_id=session.id)
                transaction.verification_status = Transaction.Status.COMPLETED
                transaction.gateway_response = session
                transaction.save()
                
                donation = transaction.donation
                donation.status = Donation.Status.SUCCESS
                donation.payment_id = session.payment_intent
                donation.save()
                
                campaign = donation.campaign
                campaign.raised_amount += donation.amount
                campaign.save()
            except Transaction.DoesNotExist:
                pass
                
        return Response(status=status.HTTP_200_OK)
