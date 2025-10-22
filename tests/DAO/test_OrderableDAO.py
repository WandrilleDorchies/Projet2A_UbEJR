class TestOrderableDAO:
    def test_create_orderable_item(self, orderable_dao, clean_database):
        orderable_id = orderable_dao.create_orderable("item")

        assert orderable_id is not None
        assert isinstance(orderable_id, int)
        assert orderable_id > 0

    def test_create_orderable_bundle(self, orderable_dao, clean_database):
        orderable_id = orderable_dao.create_orderable("bundle")

        assert orderable_id is not None
        assert isinstance(orderable_id, int)
        assert orderable_id > 0

    def test_create_multiple_orderables(self, orderable_dao, clean_database):
        id1 = orderable_dao.create_orderable("item")
        id2 = orderable_dao.create_orderable("bundle")
        id3 = orderable_dao.create_orderable("item")

        assert id1 != id2 != id3
        assert id1 < id2 < id3

    def test_orderable_id_auto_increment(self, orderable_dao, clean_database):
        ids = []
        for _ in range(5):
            orderable_id = orderable_dao.create_orderable("item")
            ids.append(orderable_id)

        for i in range(len(ids) - 1):
            assert ids[i + 1] == ids[i] + 1
