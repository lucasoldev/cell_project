from datetime import date

from django.urls import reverse

from person.models import Person


def test_person_can_be_viewed_updated_and_deleted(client, db):
    person = Person.objects.create(
        full_name='Ana Oliveira',
        address='Rua das Flores, 10',
        gender=Person.Genders.FEMALE,
        marital_status=Person.MaritalStatuses.SINGLE,
        birth_date=date(2000, 4, 15),
        phone='11999990000',
    )

    detail = client.get(
        reverse('person_detail', kwargs={'pk': person.pk})
    )
    assert detail.status_code == 200
    assert 'Ana Oliveira' in detail.content.decode()

    update = client.post(
        reverse('person_update', kwargs={'pk': person.pk}),
        {
            'full_name': 'Ana Silva',
            'address': 'Rua Nova, 20',
            'gender': Person.Genders.FEMALE,
            'marital_status': Person.MaritalStatuses.MARRIED,
            'birth_date': '2000-04-15',
            'phone': '11999990001',
            'notes': 'Cadastro atualizado',
        },
    )
    assert update.status_code == 302
    assert update.url == reverse('person_list')
    person.refresh_from_db()
    assert person.full_name == 'Ana Silva'
    assert person.phone == '11999990001'

    deletion = client.post(
        reverse('person_delete', kwargs={'pk': person.pk})
    )
    assert deletion.status_code == 302
    assert deletion.url == reverse('person_list')
    assert not Person.objects.filter(pk=person.pk).exists()

def test_create_person_saves_record_and_redirects_to_list(client, db):
    response = client.post(
        reverse('person_create'),
        {
            'full_name': 'Ana Oliveira',
            'address': 'Rua das Flores, 10',
            'gender': Person.Genders.FEMALE,
            'marital_status': Person.MaritalStatuses.SINGLE,
            'birth_date': '2000-04-15',
            'phone': '11999990000',
            'notes': '',
        },
    )

    assert response.status_code == 302
    assert response.url == reverse('person_list')
    assert Person.objects.filter(
        full_name='Ana Oliveira', phone='11999990000'
    ).exists()

def test_person_list_filters_names_without_hiding_other_matches(client, db):
    Person.objects.create(
        full_name='Ana Oliveira',
        address='Rua A',
        gender=Person.Genders.FEMALE,
        marital_status=Person.MaritalStatuses.SINGLE,
        birth_date=date(2000, 4, 15),
        phone='1111111111',
    )
    Person.objects.create(
        full_name='Ana Souza',
        address='Rua B',
        gender=Person.Genders.FEMALE,
        marital_status=Person.MaritalStatuses.SINGLE,
        birth_date=date(2001, 5, 20),
        phone='2222222222',
    )
    Person.objects.create(
        full_name='Bruno Lima',
        address='Rua C',
        gender=Person.Genders.MALE,
        marital_status=Person.MaritalStatuses.MARRIED,
        birth_date=date(1998, 8, 3),
        phone='3333333333',
    )

    response = client.get(reverse('person_list'), {'full_name': 'ana'})

    assert response.status_code == 200
    assert [person.full_name for person in response.context['persons']] == [
        'Ana Oliveira',
        'Ana Souza',
    ]
