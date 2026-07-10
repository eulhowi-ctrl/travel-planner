from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User, UserProfile
from app.schemas import (
    UserCreate,
    UserResponse,
    UserFullResponse,
    UserUpdate,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    Token,
)
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
)

router = APIRouter()


# ==================== Register Endpoint ====================
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    회원가입 엔드포인트

    - **email**: 이메일 (유니크)
    - **username**: 사용자 이름 (유니크)
    - **password**: 비밀번호 (해싱되어 저장)
    """
    # 이메일 중복 확인
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다."
        )

    # 사용자명 중복 확인
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다."
        )

    # 새 사용자 생성
    try:
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="사용자 생성 중 오류가 발생했습니다."
        )


# ==================== Login Endpoint ====================
@router.post("/login", response_model=Token)
async def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    로그인 엔드포인트

    - **email**: 사용자 이메일
    - **password**: 사용자 비밀번호

    반환: JWT access token
    """
    # 사용자 찾기
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다."
        )

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==================== Get Current User ====================
@router.get("/me", response_model=UserFullResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    현재 로그인한 사용자 정보 조회
    """
    return current_user


# ==================== Update User Profile ====================
@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자 여행 프로필 업데이트

    - **travel_theme**: 여행 테마 (couple, family, solo, friends)
    - **family_size**: 가족 인원수
    - **has_children**: 아이 동반 여부
    - **children_ages**: 아이들 나이 [3, 8, 12]
    - **preferred_activities**: 선호하는 활동 ["hiking", "beach"]
    - **budget_level**: 예산 수준 (budget, standard, luxury)
    """
    # 사용자 프로필 확인
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    if not profile:
        # 프로필이 없으면 생성
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    # 제공된 필드만 업데이트
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


# ==================== Get User Profile ====================
@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자 여행 프로필 조회
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    if not profile:
        # 프로필이 없으면 기본값으로 생성
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


# ==================== Create User Profile ====================
@router.post("/profile", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자 여행 프로필 생성

    - **travel_theme**: 여행 테마 (couple, family, solo, friends)
    - **family_size**: 가족 인원수
    - **has_children**: 아이 동반 여부
    - **children_ages**: 아이들 나이 [3, 8, 12]
    - **preferred_activities**: 선호하는 활동 ["hiking", "beach"]
    - **budget_level**: 예산 수준 (budget, standard, luxury)
    """
    # 기존 프로필 확인
    existing_profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 프로필이 존재합니다. PUT /users/profile을 사용해 수정하세요."
        )

    # 새 프로필 생성
    new_profile = UserProfile(
        user_id=current_user.id,
        **profile_data.dict()
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# ==================== Update User Info ====================
@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자 정보 업데이트 (이메일, 사용자명, 비밀번호)
    """
    # 이메일 변경 시 중복 확인
    if user_data.email and user_data.email != current_user.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다."
            )
        current_user.email = user_data.email

    # 사용자명 변경 시 중복 확인
    if user_data.username and user_data.username != current_user.username:
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자명입니다."
            )
        current_user.username = user_data.username

    # 비밀번호 변경
    if user_data.password:
        current_user.hashed_password = get_password_hash(user_data.password)

    db.commit()
    db.refresh(current_user)

    return current_user


# ==================== Deactivate Account ====================
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자 계정 비활성화
    """
    current_user.is_active = False
    db.commit()

    return {"message": "계정이 비활성화되었습니다."}
