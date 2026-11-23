package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolEntireEntity;

public interface SchoolDao{
    SchoolEntity save(SchoolEntity school);

    Optional<SchoolEntity> findBySchoolId(String schoolId);
    
    Optional<SchoolEntireEntity> findById(Integer id);
    
    boolean existsBySchoolId(String schoolId);
    
    List<SchoolEntireEntity> findTop50SchoolsByPriorityScore();

    Page<SchoolEntireEntity> findAllSchools(Pageable pageable);

    void deleteBySchoolId(String schoolId);
}