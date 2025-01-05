from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    """
    Cria um perfil automaticamente para novos usuários e garante que ele seja salvo ao atualizar o usuário.
    """
    if created:
        # Cria o perfil automaticamente para o usuário recém-criado
        Profile.objects.create(user=instance)
    else:
        # Garante que o perfil do usuário existente seja salvo ao salvar o usuário
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # Caso o perfil não exista, cria um novo perfil
            Profile.objects.create(user=instance)
