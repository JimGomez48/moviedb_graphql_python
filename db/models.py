from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    movie_credits: Mapped[list[MovieActor]] = relationship(back_populates="actor")


class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    movie_credits: Mapped[list[MovieDirector]] = relationship(back_populates="director")


class MpaaRating(Base):
    __tablename__ = "mpaa_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    movies: Mapped[list[Movie]] = relationship(back_populates="mpaa_rating")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    movie_links: Mapped[list[MovieGenre]] = relationship(back_populates="genre")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    movie_links: Mapped[list[MovieCompany]] = relationship(back_populates="company")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mpaa_rating_id: Mapped[int | None] = mapped_column(ForeignKey("mpaa_ratings.id"))

    mpaa_rating: Mapped[MpaaRating | None] = relationship(back_populates="movies")
    reviews: Mapped[list[Review]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    companies: Mapped[list[MovieCompany]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    actors: Mapped[list[MovieActor]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    directors: Mapped[list[MovieDirector]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )
    genres: Mapped[list[MovieGenre]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    reviewer: Mapped[str | None] = mapped_column(String(255))
    rating: Mapped[int | None] = mapped_column(Integer)
    body: Mapped[str | None] = mapped_column(Text)

    movie: Mapped[Movie] = relationship(back_populates="reviews")


class MovieCompany(Base):
    __tablename__ = "movie_companies"
    __table_args__ = (UniqueConstraint("movie_id", "company_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="companies")
    company: Mapped[Company] = relationship(back_populates="movie_links")


class MovieActor(Base):
    __tablename__ = "movie_actors"
    __table_args__ = (UniqueConstraint("movie_id", "actor_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="actors")
    actor: Mapped[Actor] = relationship(back_populates="movie_credits")
    roles: Mapped[list[MovieActorRole]] = relationship(
        back_populates="movie_actor", cascade="all, delete-orphan"
    )


class MovieActorRole(Base):
    __tablename__ = "movie_actor_roles"
    __table_args__ = (UniqueConstraint("movie_actor_id", "role"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_actor_id: Mapped[int] = mapped_column(
        ForeignKey("movie_actors.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(255), nullable=False)

    movie_actor: Mapped[MovieActor] = relationship(back_populates="roles")


class MovieDirector(Base):
    __tablename__ = "movie_directors"
    __table_args__ = (UniqueConstraint("movie_id", "director_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"), nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="directors")
    director: Mapped[Director] = relationship(back_populates="movie_credits")


class MovieGenre(Base):
    __tablename__ = "movie_genres"
    __table_args__ = (UniqueConstraint("movie_id", "genre_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="genres")
    genre: Mapped[Genre] = relationship(back_populates="movie_links")
