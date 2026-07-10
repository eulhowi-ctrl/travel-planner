from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Dict
from decimal import Decimal

from app.database import get_db
from app.models import Budget, Itinerary, User
from app.schemas import BudgetResponse, BudgetCreate, BudgetUpdate, BudgetSummary
from app.auth import get_current_active_user

router = APIRouter()


# ==================== Add Budget Item ====================
@router.post("/itineraries/{itinerary_id}/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def add_budget_item(
    itinerary_id: int,
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획에 예산 항목 추가

    **Categories:**
    - flight: 항공료
    - accommodation: 숙박비
    - meal: 식사비
    - activity: 활동비
    - transport: 시내 교통비
    - shopping: 쇼핑
    - other: 기타

    예시:
    ```json
    {
      "category": "flight",
      "item_name": "인천-제주 항공권",
      "estimated_cost": 85000,
      "currency": "KRW",
      "notes": "왕복 항공권"
    }
    ```
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 예산 항목 생성
    new_budget = Budget(
        itinerary_id=itinerary_id,
        **budget_data.dict()
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget


# ==================== Get Budget Items ====================
@router.get("/itineraries/{itinerary_id}/budgets", response_model=List[BudgetResponse])
async def get_budget_items(
    itinerary_id: int,
    category: str = Query(None, description="카테고리 필터"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획의 예산 항목 조회

    Optional:
    - **category**: 특정 카테고리만 조회
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 예산 항목 조회
    query = db.query(Budget).filter(Budget.itinerary_id == itinerary_id)

    if category:
        query = query.filter(Budget.category == category)

    budgets = query.order_by(Budget.category).all()

    return budgets


# ==================== Get Budget Item Detail ====================
@router.get("/budgets/{budget_id}", response_model=BudgetResponse)
async def get_budget_item(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    예산 항목 상세 조회
    """
    budget = db.query(Budget).filter(Budget.id == budget_id).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 항목을 찾을 수 없습니다."
        )

    # 소유권 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == budget.itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 예산 항목에 접근할 수 없습니다."
        )

    return budget


# ==================== Update Budget Item ====================
@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget_item(
    budget_id: int,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    예산 항목 수정
    """
    budget = db.query(Budget).filter(Budget.id == budget_id).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 항목을 찾을 수 없습니다."
        )

    # 소유권 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == budget.itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 예산 항목을 수정할 수 없습니다."
        )

    # 업데이트
    update_data = budget_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(budget, field, value)

    db.commit()
    db.refresh(budget)

    return budget


# ==================== Delete Budget Item ====================
@router.delete("/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget_item(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    예산 항목 삭제
    """
    budget = db.query(Budget).filter(Budget.id == budget_id).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 항목을 찾을 수 없습니다."
        )

    # 소유권 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == budget.itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 예산 항목을 삭제할 수 없습니다."
        )

    db.delete(budget)
    db.commit()

    return {"message": "예산 항목이 삭제되었습니다."}


# ==================== Get Budget Summary ====================
@router.get("/itineraries/{itinerary_id}/budget-summary", response_model=BudgetSummary)
async def get_budget_summary(
    itinerary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획의 예산 요약

    Returns:
    - total_estimated: 예상 총 예산
    - total_actual: 실제 사용 비용 (입력한 경우)
    - remaining_budget: 남은 예산
    - by_category: 카테고리별 상세 예산
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 예산 항목 조회
    budgets = db.query(Budget).filter(
        Budget.itinerary_id == itinerary_id
    ).all()

    # 예산 계산
    total_estimated = sum(b.estimated_cost for b in budgets) if budgets else 0
    total_actual = sum(b.actual_cost for b in budgets if b.actual_cost) if budgets else 0
    remaining_budget = (itinerary.budget_allocated or total_estimated) - total_actual

    # 카테고리별 예산
    by_category = {}
    for budget in budgets:
        if budget.category not in by_category:
            by_category[budget.category] = {
                "estimated": 0,
                "actual": 0,
                "count": 0
            }

        by_category[budget.category]["estimated"] += budget.estimated_cost
        by_category[budget.category]["actual"] += budget.actual_cost or 0
        by_category[budget.category]["count"] += 1

    return BudgetSummary(
        total_estimated=total_estimated,
        total_actual=total_actual if total_actual > 0 else None,
        remaining_budget=remaining_budget if itinerary.budget_allocated else None,
        by_category=by_category
    )


# ==================== Budget Statistics ====================
@router.get("/itineraries/{itinerary_id}/budget-stats", response_model=dict)
async def get_budget_statistics(
    itinerary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    예산 통계 및 분석
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 예산 항목 조회
    budgets = db.query(Budget).filter(
        Budget.itinerary_id == itinerary_id
    ).all()

    if not budgets:
        return {
            "total_items": 0,
            "total_estimated": 0,
            "total_actual": 0,
            "spent_percentage": 0,
            "by_category": {}
        }

    total_estimated = sum(b.estimated_cost for b in budgets)
    total_actual = sum(b.actual_cost for b in budgets if b.actual_cost)
    spent_percentage = (total_actual / total_estimated * 100) if total_estimated > 0 else 0

    # 카테고리별 통계
    by_category = {}
    category_counts = {}

    for budget in budgets:
        category = budget.category
        if category not in by_category:
            by_category[category] = {
                "estimated": 0,
                "actual": 0
            }
            category_counts[category] = 0

        by_category[category]["estimated"] += budget.estimated_cost
        by_category[category]["actual"] += budget.actual_cost or 0
        category_counts[category] += 1

    # 카테고리별 비율
    for category in by_category:
        total_cat_estimated = by_category[category]["estimated"]
        by_category[category]["percentage"] = (
            total_cat_estimated / total_estimated * 100
        ) if total_estimated > 0 else 0

    return {
        "total_items": len(budgets),
        "total_estimated": total_estimated,
        "total_actual": total_actual,
        "spent_percentage": round(spent_percentage, 2),
        "by_category": by_category,
        "allocated_budget": itinerary.budget_allocated,
        "budget_status": _get_budget_status(total_estimated, itinerary.budget_allocated)
    }


# ==================== Currency Conversion ====================
@router.get("/currency-convert", response_model=dict)
async def convert_currency(
    amount: float = Query(..., gt=0),
    from_currency: str = Query("KRW"),
    to_currency: str = Query("USD")
):
    """
    통화 환율 변환

    환율 기준 (실시간 업데이트 필요):
    - KRW (한국원)
    - USD (미국 달러)
    - JPY (일본 엔)
    - CNY (중국 위안)
    - THB (태국 바트)
    - SGD (싱가포르 달러)
    - EUR (유로)

    Example:
    ```
    /api/v1/budgets/currency-convert?amount=100000&from_currency=KRW&to_currency=USD
    ```
    """
    # 환율 정보 (2026-07-10 기준, 실시간 업데이트 필요)
    exchange_rates = {
        "KRW": 1.0,
        "USD": 0.00077,
        "JPY": 0.11,
        "CNY": 0.0055,
        "THB": 0.028,
        "SGD": 0.0010,
        "EUR": 0.00071
    }

    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"지원하지 않는 통화입니다. 지원 통화: {list(exchange_rates.keys())}"
        )

    # 환전 계산
    amount_in_krw = amount / exchange_rates[from_currency]
    converted_amount = amount_in_krw * exchange_rates[to_currency]

    return {
        "original_amount": amount,
        "from_currency": from_currency,
        "converted_amount": round(converted_amount, 2),
        "to_currency": to_currency,
        "exchange_rate": round(exchange_rates[to_currency] / exchange_rates[from_currency], 6),
        "note": "이 환율은 참고용이며, 실제 환율은 금융 기관에 확인하세요."
    }


# ==================== Helper Functions ====================
def _get_budget_status(estimated: float, allocated: float) -> str:
    """예산 상태 판정"""
    if not allocated:
        return "예산 미설정"

    ratio = estimated / allocated
    if ratio <= 0.8:
        return "낮음"
    elif ratio <= 1.0:
        return "적정"
    elif ratio <= 1.2:
        return "주의"
    else:
        return "초과"


# ==================== Budget Tips ====================
@router.get("/budget-tips", response_model=List[str])
async def get_budget_tips():
    """
    예산 관리 팁
    """
    tips = [
        "항공권은 가능한 한 미리 예약하세요 (1-2개월 전)",
        "여행지의 물가를 미리 조사하고 예산을 설정하세요",
        "숙박비는 총 여행비의 40%를 목표로 하세요",
        "식사비는 총 여행비의 30%를 목표로 하세요",
        "활동비는 총 여행비의 20%를 목표로 하세요",
        "예상치 못한 비용을 위해 여유 자금을 준비하세요 (10%)",
        "현지 교통카드를 구입하면 교통비를 절약할 수 있습니다",
        "관광지 주변 식당보다 현지인 식당이 더 저렴합니다",
        "프리투어 대신 셀프 투어로 활동비를 절약하세요",
        "여행 중 환전은 환전소에서 하는 것이 은행보다 저렴합니다"
    ]
    return tips
