package com.schoolrde.schoolservice.dao.bussiness;

import java.util.Optional;
import com.schoolrde.schoolservice.entity.SchoolEntity;

public interface SchoolDao{
    SchoolEntity save(SchoolEntity school);

    Optional<SchoolEntity> findBySchoolId(String schoolId);

    boolean existsBySchoolId(String schoolId);

    void deleteBySchoolId(String schoolId);
}