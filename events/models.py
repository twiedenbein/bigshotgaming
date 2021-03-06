from django.db import models
from django.core.mail import send_mail
from localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader, Context
from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from paypal.standard.ipn.models import PayPalIPN
import uuid
import datetime

def make_uuid():
        return unicode(uuid.uuid4())

class Event(models.Model):

    def __unicode__(self):
        return self.name
        
    def number_pending(self):
        return self.participant_set.filter(coupon__isnull=True).count()
    
    def number_paid(self):
        return self.coupon_set.all().count()
        
    def number_remaining(self):
        return self.participant_limit - self.number_paid()
    
    name = models.CharField(max_length=100, verbose_name='Event Name')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.ForeignKey('Venue')
    participant_limit = models.IntegerField()
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    registration_enabled = models.BooleanField(default=False)
    prepay_price = models.DecimalField(max_digits=4, decimal_places=2)
    atd_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='At-the-Door price')
    waiver = models.FileField(upload_to='events/waivers/', blank=True)
    
class Venue(models.Model):
    
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=30)
    state = USStateField()
    zipcode = models.CharField(max_length=10)

class ParticipantManager(models.Manager):
    def get_by_natural_key(self, user, event):
        return self.get(user=user.username, event=event.name)

class Participant(models.Model):
    
    def __unicode__(self):
        return '%s - %s' % (self.user.username, self.event)

    def natural_key(self):
        return (self.user.username, self.event.name)
    
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    coupon = models.OneToOneField('Coupon', blank=True, null=True)
    signup_time = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)
    checkin_time = models.DateTimeField(blank=True, null=True)

class Coupon(models.Model):
    
    def __unicode__(self):
        return self.uuid
    
    def activate(self):
        self.activated = True
        self.activated_time = datetime.datetime.now()
        self.save()
        
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    event = models.ForeignKey(Event)
    paypal_transaction = models.ForeignKey(PayPalIPN, blank=True, null=True, editable=False)
    stripe_transaction = models.CharField(max_length=128, blank=True, null=True, editable=False)
    activated = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    activated_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

class Waiver(models.Model):
    def __unicode__(self):
        return '%s\'s waiver signed %s' % (self.part.user.username, self.signed_on)

    part = models.ForeignKey(Participant)
    name = models.CharField(max_length=255)
    pname = models.CharField(max_length=255, blank=True, null=True)
    minor = models.BooleanField(default=False)
    minor_age = models.IntegerField(max_length=2, blank=True, null=True)
    signed_on = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Event)
def one_active(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_active is True:
        Event.objects.exclude(pk=instance.pk).update(is_active=False)
    
@receiver(payment_was_successful)
def payment_complete(sender, **kwargs):
    user = User.objects.get(username=sender.custom)
    event = Event.objects.get(is_active=True)
    # we do this so that the Coupon objects actually have their correct types
    coupons = [Coupon(transaction=sender, event=event) for i in xrange(sender.quantity)]
    for coupon in coupons:
        coupon.save()
    # I cannot see a better way to do this at the moment, so here we are
    # We pop the last coupon off the list to activate the ticket for the original payer
    participant = Participant.objects.get_or_create(user=user, event=event)[0]
    coupon = coupons.pop()
    activate_coupon(participant, coupon)
    # We need to dispatch off an email...
    email_confirmation(participant=participant, coupons=coupons)

@receiver(payment_was_flagged)
def payment_flagged(sender, **kwargs):
    print sender
    print "Something went wrong..."
    
def activate_coupon(participant, coupon):
    participant.coupon = coupon
    coupon.activate()
    participant.save()
    
def email_confirmation(**kwargs):
    t = loader.get_template('events/email.txt')
    if 'participant' in kwargs:
        user = kwargs['participant'].user
        event = kwargs['participant'].event
        
    c = Context({
        'username': user.username,
        'event': event,
    })
    
    if len(kwargs['coupons']) > 0:
        c['coupons'] = kwargs['coupons']
    
    subj = '%s registration confirmation' % event.name
    fr = 'Big Shot Gaming <bigshot@bigshotgaming.com>'
    send_mail(subj, t.render(c), fr, [user.email])
    
    
    
