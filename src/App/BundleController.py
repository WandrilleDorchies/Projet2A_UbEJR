from fastapi import APIRouter, HTTPException, status

from src.App.init_app import bundle_service

bundle_router = APIRouter(prefix="/bundles", tags=["Bundles"])


# get bundle by id
@bundle_router.get("/{bundle_id}", status_code=status.HTTP_200_OK)
def get_bundle_by_id(bundle_id: int):
    try:
        bundle = bundle_service.get_bundle(bundle_id)
        return bundle
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Bundle with id [{}] not found".format(bundle_id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception


# get all bundles
@bundle_router.get("/", status_code=status.HTTP_200_OK)
def get_all_bundles():
    try:
        bundles = bundle_service.get_all_bundles()
        if bundles is None:
            raise HTTPException(status_code=404, detail="No bundles !")
        return bundles

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception


# create bundle
def create_bundle():
    pass
