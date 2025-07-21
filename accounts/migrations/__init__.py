from django.utils.translation import gettext_lazy as _


class UserEvents:
    """The different user event types."""

    # Account related events
    ACCOUNT_CREATED = "account_created"
    PASSWORD_RESET_LINK_SENT = "password_reset_link_sent"
    PASSWORD_RESET = "password_reset"
    PASSWORD_CHANGED = "password_changed"
    EMAIL_CHANGE_REQUEST = "email_changed_request"
    EMAIL_CHANGED = "email_changed"
    ACCOUNT_DELETE_REQUEST = "account_delete_request"
    
    # Tag user releted events
    USER_TAG_ASSIGNED = "user_tag_assigned"
    USER_TAG_LOST = "user_tag_lost"
    USER_TAG_FOUND = "user_tag_found"
    USER_TAG_RECOVERED = "user_tag_recovered"
    
    # Staff actions over customers events
    CUSTOMER_DELETED = "customer_deleted"  # staff user deleted a user account
    EMAIL_ASSIGNED = "email_assigned"  # the staff user assigned a email to the user account
    NAME_ASSIGNED = "name_assigned"  # the staff user added set a name to the user account
    NOTE_ADDED = "note_added"  # the staff user added a note to the user account
    
    CHOICES = [
        (ACCOUNT_CREATED, _("Acest cont a fost creat")),
        (
            PASSWORD_RESET_LINK_SENT, 
            _("Linkul de resetare parolă a fost trimis pe emailul utilizatorului")
        ),
        (PASSWORD_RESET, _("Parola contului a fost resetată")),
        (
            EMAIL_CHANGE_REQUEST,
            "Utiliziatorul a cerut schimbarea parolei.",
        ),
        (PASSWORD_CHANGED, _("Parola acestui cont a fost schimbată")),
        (EMAIL_CHANGED, _("Adresa de email asociată contului a fost schimbată")),
        (
            ACCOUNT_DELETE_REQUEST, 
            _("A fost trimisă cerere de ștergere a contului")
        ),
        (USER_TAG_ASSIGNED, _("TAGul a fost acosiat contului")),
        (USER_TAG_LOST, _("TAGul a fost declatat pierdut")),
        (USER_TAG_FOUND, _("TAGul a fost declatat găsit")),
        (USER_TAG_RECOVERED, _("TAGul a fost declatat recuperat")),
        (CUSTOMER_DELETED, _("Utilizatorul a fost sters")),
        (EMAIL_ASSIGNED, _("A customer's email address was edited")),
        (NAME_ASSIGNED, _("Numele utilizatorului a fost editat")),
        (NOTE_ADDED, _("O notă a fost adaugata cleintului")),
    ]
    
class UserFormErrors:
    missing_email = {'required':_('Introduceți o adresa de email validă!')}