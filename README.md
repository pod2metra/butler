# Installation 

```
pip install -e git@github.com:pod2metra/butler.git#egg=butler
```

# Configuration 

```
set 'butler' into installed apps 
```

# Inherit your user profile class from butler class

```
from butler.models import ButlerProfile 

class UserPropfile(ButlerProfile):
    pass 
```
