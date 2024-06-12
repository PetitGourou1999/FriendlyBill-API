from data.models import User, MODELS

def test_create_admin_no_flag(runner):
    result = runner.invoke(args='admin')
    assert not result.output
    
def test_create_admin_already_exists_abort(runner, user_admin):
    result = runner.invoke(args=['admin', '--create'], input='N\n')
    assert result.exit_code == 1
    assert 'Aborted!' in result.output

def test_create_admin_email_not_valid(runner):
    result = runner.invoke(args=['admin', '--create'], input='Hello World!\n')
    assert result.exit_code == 2
    assert 'Email is not valid' in result.output

def test_create_admin_email_already_taken(runner, user_admin, user_admin_email):
    result = runner.invoke(args=['admin', '--create'], input='y\n{}\n'.format(user_admin_email))
    assert result.exit_code == 2
    assert 'Email already taken' in result.output
    
def test_create_admin(runner):
    result = runner.invoke(args=['admin', '--create'], input='admin@admin.com\nAdmin\nAdmin\npassword\npassword')
    assert result.exit_code == 0
    assert 'User added' in result.output
    
    new_admin = User.get_by_email('admin@admin.com')
    assert new_admin
    assert new_admin.is_superadmin is True

def test_create_admin_already_exists(runner, user_admin):
    result = runner.invoke(args=['admin', '--create'], input='y\nother.admin@admin.com\nAdmin\nAdmin\npassword\npassword')
    assert result.exit_code == 0
    assert 'User added' in result.output
    
    new_admin = User.get_by_email('other.admin@admin.com')
    assert new_admin
    assert new_admin.is_superadmin is True
    
def test_create_database_no_flag(runner):
    result = runner.invoke(args='database')
    assert not result.output

def test_create_database(runner):
    result = runner.invoke(args=['database', '--create'])
    assert result.exit_code == 0
    
    for model in MODELS:
        query = model.select().execute()
        assert len(list(query)) == 0

def test_reset_database_(runner, all_data):
    result = runner.invoke(args=['database', '--reset'])
    assert result.exit_code == 0
    
    for model in MODELS:
        query = model.select().execute()
        assert len(list(query)) == 0
