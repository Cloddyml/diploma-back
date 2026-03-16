import pytest

from app.exceptions.excs import ObjectAlreadyExistsException, ObjectNotFoundException
from app.schemas import (
    TopicAddRequestDto,
    TopicDto,
    TopicPatchRequestDto,
    TopicPutRequestDto,
)
from app.utils.db_manager import DBManager

# --- Фикстура с тестовым топиком ---------------------------------------------------


@pytest.fixture
async def topic(db: DBManager) -> TopicDto:
    await db.topics.add(
        TopicAddRequestDto(
            slug="python",
            title="Python",
            content="Основы Python",
            order_index=1,
            is_published=True,
        )
    )
    await db.commit()
    return await db.topics.get_one_or_none(slug="python")


# --- get_all ---------------------------------------------------


async def test_get_all_returns_empty_list(db: DBManager):
    result = await db.topics.get_all()
    assert result == []


async def test_get_all_returns_all_topics(db: DBManager):
    await db.topics.add(TopicAddRequestDto(slug="python", title="Python"))
    await db.topics.add(TopicAddRequestDto(slug="fastapi", title="FastAPI"))
    await db.commit()

    result = await db.topics.get_all()

    assert len(result) == 2
    slugs = {t.slug for t in result}
    assert slugs == {"python", "fastapi"}


# --- get_one_or_none ---------------------------------------------------


async def test_get_one_or_none_returns_topic(db: DBManager, topic: TopicDto):
    result = await db.topics.get_one_or_none(slug="python")

    assert result is not None
    assert result.slug == "python"
    assert result.title == "Python"


async def test_get_one_or_none_returns_none_if_not_found(db: DBManager):
    result = await db.topics.get_one_or_none(slug="nonexistent")

    assert result is None


# --- add ---------------------------------------------------


async def test_add_topic(db: DBManager):
    await db.topics.add(TopicAddRequestDto(slug="django", title="Django"))
    await db.commit()

    result = await db.topics.get_one_or_none(slug="django")

    assert result is not None
    assert result.slug == "django"
    assert result.title == "Django"


async def test_add_topic_default_values(db: DBManager):
    await db.topics.add(TopicAddRequestDto(slug="django", title="Django"))
    await db.commit()

    result = await db.topics.get_one_or_none(slug="django")

    assert result.order_index == 0
    assert result.is_published is False
    assert result.content is None


async def test_add_topic_duplicate_slug_raises(db: DBManager, topic: TopicDto):
    with pytest.raises(ObjectAlreadyExistsException):
        await db.topics.add(TopicAddRequestDto(slug="python", title="Python 2"))
        await db.commit()


# --- edit (PUT) ---------------------------------------------------


async def test_edit_topic(db: DBManager, topic: TopicDto):
    await db.topics.edit(
        id=topic.id,
        data=TopicPutRequestDto(
            slug="python-advanced",
            title="Python Advanced",
            content="Продвинутый Python",
            order_index=2,
            is_published=False,
        ),
    )
    await db.commit()

    result = await db.topics.get_one_or_none(id=topic.id)

    assert result.slug == "python-advanced"
    assert result.title == "Python Advanced"
    assert result.content == "Продвинутый Python"
    assert result.order_index == 2
    assert result.is_published is False


async def test_edit_topic_not_found_raises(db: DBManager):
    with pytest.raises(ObjectNotFoundException):
        await db.topics.edit(
            id=99999,
            data=TopicPutRequestDto(
                slug="ghost",
                title="Ghost",
                order_index=0,
                is_published=False,
            ),
        )


# --- edit (PATCH) ---------------------------------------------------


async def test_partial_edit_topic_only_title(db: DBManager, topic: TopicDto):
    await db.topics.edit(
        id=topic.id,
        data=TopicPatchRequestDto(title="Новый заголовок"),
        exclude_unset=True,
    )
    await db.commit()

    result = await db.topics.get_one_or_none(id=topic.id)

    assert result.title == "Новый заголовок"
    assert result.slug == "python"  # не изменился


async def test_partial_edit_topic_not_found_raises(db: DBManager):
    with pytest.raises(ObjectNotFoundException):
        await db.topics.edit(
            id=99999,
            data=TopicPatchRequestDto(title="Ghost"),
            exclude_unset=True,
        )


# --- delete ---------------------------------------------------


async def test_delete_topic(db: DBManager, topic: TopicDto):
    await db.topics.delete(id=topic.id)
    await db.commit()

    result = await db.topics.get_one_or_none(id=topic.id)

    assert result is None


async def test_delete_topic_not_found_raises(db: DBManager):
    with pytest.raises(ObjectNotFoundException):
        await db.topics.delete(id=99999)


# --- get_filtered ---------------------------------------------------


async def test_get_filtered_by_is_published(db: DBManager):
    from app.models import TopicsOrm

    await db.topics.add(
        TopicAddRequestDto(slug="published", title="Published", is_published=True)
    )
    await db.topics.add(
        TopicAddRequestDto(slug="draft", title="Draft", is_published=False)
    )
    await db.commit()

    result = await db.topics.get_filtered(TopicsOrm.is_published)

    assert all(t.is_published for t in result)
    slugs = {t.slug for t in result}
    assert "published" in slugs
    assert "draft" not in slugs
