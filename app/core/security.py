from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="seller/token")
oauth2_scheme_delivery_partner = OAuth2PasswordBearer(tokenUrl="delivery-partner/token")