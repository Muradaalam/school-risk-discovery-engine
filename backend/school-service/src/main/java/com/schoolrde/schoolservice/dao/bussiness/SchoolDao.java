package com.schoolrde.schoolservice.dao.bussiness;

import java.util.Optional;
import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolEntireEntity;

public interface SchoolDao{
    SchoolEntity save(SchoolEntity school);

    Optional<SchoolEntity> findBySchoolId(String schoolId);
    
    Optional<SchoolEntireEntity> findById(Integer id);
    
    boolean existsBySchoolId(String schoolId);

    void deleteBySchoolId(String schoolId);
}